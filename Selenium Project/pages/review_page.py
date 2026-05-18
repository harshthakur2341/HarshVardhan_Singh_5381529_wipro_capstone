from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.navigation import NavigationHandler

class ReviewPage(BasePage):
    PROCEED_PAYMENT_BTN = (By.XPATH, "//button[contains(text(),'Proceed to Payment')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.nav_handler = NavigationHandler(driver, logger)

    def proceed_to_payment(self):
        self.safe_click(self.PROCEED_PAYMENT_BTN)
        self.nav_handler.handle_page_transition("railways/payment")
        self.logger.info("Navigated to Payment page")
