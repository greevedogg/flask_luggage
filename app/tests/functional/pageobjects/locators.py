from selenium.webdriver.common.by import By


class GlobalLocators(object):
    CLOSE_TICKET_INITIALS = (By.ID, 'dialog__close-ticket-initials')
    CLOSE_TICKET = (By.XPATH, '//button[contains(@class,"dialog__close-ticket__close")]')


class MainPageLocators(GlobalLocators):
    """All main page locators should come here"""
    STORE_BUTTON = (By.ID, 'submit')
    TICKET = (By.ID, 'ticket')
    LOGGED_IN_BY = (By.ID, 'loggedInBy')
    LOCATION = (By.ID, 'location')
    BAG_COUNT = (By.ID, 'bagCount')
    NAME = (By.ID, 'name')
    TICKET_ROW = (By.ID, 'ticket-number-{0}')
    TICKET_ACTION_BUTTON = (By.XPATH, '//button[contains(@class,"ticket-action-button") and @data-ticket-number="{0}"]')
    TICKET_COMPLETE_BUTTON = (By.XPATH, 'id("ticket-number-{0}")//*[contains(@class, "ticket-actions__complete")]')
    MODIFY_TICKET = (By.XPATH, 'id("ticket-number-{0}")//*[contains(@class, "ticket-actions__modify")]')


class EditTicketPageLocators(GlobalLocators):
    """All edit ticket page locators should come here"""
    STORE_BUTTON = (By.ID, 'submit')
