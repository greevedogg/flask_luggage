from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from locators import MainPageLocators


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class TicketElement(BasePageElement):
    """This class gets the ticket # form field from the specified locator"""
    locator = MainPageLocators.TICKET


class NameElement(BasePageElement):
    """This class gets the name form field from the specified locator"""
    locator = MainPageLocators.NAME


class BagCountElement(BasePageElement):
    """This class gets the bag count form field from the specified locator"""
    locator = MainPageLocators.BAG_COUNT


class LocationElement(BasePageElement):
    """This class gets the location form field from the specified locator"""
    locator = MainPageLocators.LOCATION


class LoggedInByElement(BasePageElement):
    """This class gets the logged in by form field from the specified locator"""
    locator = MainPageLocators.LOGGED_IN_BY


class CloseTicketInitialsElement(BasePageElement):
    """This class gets the logged in by form field from the specified locator"""
    locator = MainPageLocators.CLOSE_TICKET_INITIALS
