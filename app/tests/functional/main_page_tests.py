import unittest
from appium import webdriver
from pageobjects.pages import MainPage
import bootstrap.common as env


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            env.SELENIUM_HUB,
            env.CAPABILITIES
        )
        self.driver.implicitly_wait(10 if 'ios' not in env.platform else 60)
        self.ticket_number = "46789254"

    def test_01_search_in_python_org(self):
        driver = self.driver
        driver.get(env.APP_BASE_URL)
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
        driver.get(env.APP_BASE_URL)

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