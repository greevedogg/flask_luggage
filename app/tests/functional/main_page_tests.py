import unittest
from appium import webdriver
import os
from pageobjects.pages import MainPage

http_user = os.environ.get('HTTP_USER', '')
http_pass = os.environ.get('HTTP_PASS', '')
platform = os.environ.get('PLATFORM', '')

APPIUM_STANDALONE = 'http://172.16.0.101:4723/wd/hub'
SELENIUM_GRID_HUB = 'http://172.16.0.101:4444/wd/hub'
IS_PRODUCTION = True

APP_BASE_URL = 'https://{0}:{1}@lotsaluggage.net'.format(http_user, http_pass) \
    if IS_PRODUCTION else 'http://localhost:5000'


SELENIUM_HUB = SELENIUM_GRID_HUB if 'ios' not in platform else APPIUM_STANDALONE

if 'ios' in platform:
    CAPABILITIES = {
      'platformName': 'iOS',
      'platformVersion': '9.2',
      'browserName': 'Safari',
      'deviceName': 'iPad Air 2',
      'safariIgnoreFraudWarning': True,
      'nonSyntheticWebClick': True
    }
else:
    CAPABILITIES = {
        'platformName': 'MAC',
        'browserName': 'firefox'
    }


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            SELENIUM_HUB,
            CAPABILITIES
        )
        self.driver.implicitly_wait(10 if 'ios' not in platform else 60)
        self.ticket_number = "46789254"

    def tes_01_search_in_python_org(self):
        driver = self.driver
        driver.get(APP_BASE_URL)
        ticket_number = self.ticket_number

        main_page = MainPage(driver)

        assert main_page.is_title_matches()

        main_page.ticket = ticket_number
        main_page.name = "COLON"
        main_page.bag_count = "2"
        main_page.location = "12A"
        main_page.logged_in_by = "JC"
        main_page.store_ticket()

        assert main_page.has_stored_ticked(ticket_number)

    def test_02_complete_ticket(self):
        driver = self.driver
        driver.get(APP_BASE_URL)

        ticket_number = self.ticket_number

        main_page = MainPage(driver)
        main_page.ask_for_initials(ticket_number)
        main_page.close_ticket_initials = "JC"
        main_page.close_ticket()

    def tearDown(self):
        self.driver.quit()
        pass

if __name__ == "__main__":
    unittest.main()