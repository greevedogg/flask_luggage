from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from elements import (TicketElement, NameElement, BagCountElement, LocationElement, LoggedInByElement,
                      CloseTicketInitialsElement)
from locators import MainPageLocators, EditTicketPageLocators
from time import sleep
from bootstrap.common import platform
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


IS_IOS = True if 'ios' in platform else False

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        if IS_IOS:
            driver.orientation = 'LANDSCAPE'

        self.driver = driver

    def select_location(self, *locations):
        view_location_button = self.driver.find_element(*MainPageLocators.VIEW_LOCATION)
        view_location_button.click()

        prepared_locations = self._get_formatted_bin_locations(MainPageLocators.BIN_LOCATION, locations)

        if len(prepared_locations) > 1:
            if not IS_IOS:
                action = ActionChains(self.driver)

                for i, location in enumerate(prepared_locations):
                    action.click(self.driver.find_element(*location))

                    # hold meta click after clicking the first bin so pre-selected bins will reset
                    if i == 0:
                        action.key_down(Keys.META)

                action.key_up(Keys.META)

                action.click(self.driver.find_element(*MainPageLocators.SAVE_BINS))
                action.perform()
            else:
                # sleep(2)

                bin_mapping = {
                    '21a': {'x': 75, 'y': 166},
                    '21b': {'x': 75, 'y': 251},
                    '22a': {'x': 184, 'y': 166},
                    '22b': {'x': 184, 'y': 251},
                }

                bin_actions = []

                self.driver.switch_to.context('NATIVE_APP')

                for i, location in enumerate(locations):
                    bin_action1 = TouchAction(self.driver)
                    bin_action1.press(**bin_mapping[location]).release()

                    if i == 0:
                        TouchAction(self.driver).tap(**bin_mapping[location]).perform()

                    bin_actions.append(bin_action1)



                ma = MultiAction(self.driver)
                ma.add(*bin_actions)
                ma.perform()
                self.driver.switch_to.context(self.driver.contexts[1])

                self.driver.find_element(*MainPageLocators.SAVE_BINS).click()

                sleep(1)

        # if IS_IOS:
        #     sleep(10)

    @staticmethod
    def _get_formatted_bin_locations(locater_template, locations):
        return [
            (locater_template[0], locater_template[1].format(value))
            for i, value in enumerate(locations)
        ]


class EditTicketPage(BasePage):
    close_ticket_initials = CloseTicketInitialsElement()

    def ask_for_initials(self):
        button = self.driver.find_element(*EditTicketPageLocators.STORE_BUTTON)
        button.click()
        sleep(1) if IS_IOS else sleep(1)

    def modify_ticket(self):
        self.driver.find_element(*EditTicketPageLocators.CLOSE_TICKET).click()


class MainPage(BasePage):
    ticket = TicketElement()
    name = NameElement()
    bag_count = BagCountElement()
    location = LocationElement()
    logged_in_by = LoggedInByElement()
    close_ticket_initials = CloseTicketInitialsElement()

    def is_title_matches(self):
        """Verifies that the hardcoded text "Luggage" appears in page title"""
        return "Luggage" in self.driver.title

    def store_ticket(self):
        sleep(2) if IS_IOS else sleep(1)
        element = self.driver.find_element(*MainPageLocators.STORE_BUTTON)
        element.click()

    def has_stored_ticked(self, ticket_number):
        ticket_row = [
            value.format(ticket_number) if i == 1 else value
            for i, value in enumerate(MainPageLocators.TICKET_ROW)
        ]
        return self.driver.find_element(*ticket_row)

    def ask_for_initials(self, ticket_number):
        TICKET_ROW = self._get_formatted_locator(ticket_number, MainPageLocators.TICKET_ROW)
        TICKET_ACTION_BUTTON = self._get_formatted_locator(ticket_number, MainPageLocators.TICKET_ACTION_BUTTON)
        TICKET_COMPLETE_BUTTON = self._get_formatted_locator(ticket_number, MainPageLocators.TICKET_COMPLETE_BUTTON)

        self.driver.find_element(*TICKET_ROW)
        actions_element = self.driver.find_element(*TICKET_ACTION_BUTTON)
        actions_element.click()

        complete_button = self.driver.find_element(*TICKET_COMPLETE_BUTTON)
        complete_button.click()

    def modify_ticket_url(self, ticket_number):
        MODIFY_TICKET = self._get_formatted_locator(ticket_number, MainPageLocators.MODIFY_TICKET)
        modify_link = self.driver.find_element(*MODIFY_TICKET)

        return modify_link.get_attribute('href')

    def close_ticket(self):
        self.driver.find_element(*MainPageLocators.CLOSE_TICKET).click()

    @staticmethod
    def _get_formatted_locator(ticket_number, locator):
        return [
            value.format(ticket_number) if i == 1 else value
            for i, value in enumerate(locator)
        ]


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source
