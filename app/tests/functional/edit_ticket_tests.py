import unittest
from appium import webdriver
from pageobjects.pages import MainPage, EditTicketPage
import env


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

    def tes_02_edit_ticket(self):
        driver = self.driver
        driver.get(env.APP_BASE_URL)

        ticket_number = self.ticket_number

        main_page = MainPage(driver)
        modify_ticket_url = main_page.modify_ticket_url(ticket_number)

        driver.get(modify_ticket_url)

        edit_ticket = EditTicketPage(driver)
        edit_ticket.ask_for_initials()
        edit_ticket.close_ticket_initials = "RG"
        edit_ticket.modify_ticket()

    def tearDown(self):
        self.driver.quit()
        pass

if __name__ == "__main__":
    unittest.main()