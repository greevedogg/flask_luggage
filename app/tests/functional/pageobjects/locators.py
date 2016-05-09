from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    STORE_BUTTON = (By.ID, 'submit')
    TICKET = (By.ID, 'ticket')
    LOGGED_IN_BY = (By.ID, 'loggedInBy')
    LOCATION = (By.ID, 'location')
    BAG_COUNT = (By.ID, 'bagCount')
    NAME = (By.ID, 'name')
    TICKET_ROW = (By.ID, 'ticket-number-{0}')
    TICKET_ACTION_BUTTON = (By.XPATH, '//button[contains(@class,"ticket-action-button") and @data-ticket-number="{0}"]')
    TICKET_COMPLETE_BUTTON = (By.XPATH, 'id("ticket-number-{0}")//*[contains(@class, "ticket-actions__complete")]')
    CLOSE_TICKET_INITIALS = (By.ID, 'dialog__close-ticket-initials')
    CLOSE_TICKET = (By.XPATH, '//button[contains(@class,"dialog__close-ticket__close")]')


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass
