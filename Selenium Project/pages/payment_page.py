from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PaymentPage(BasePage):
    CREDIT_CARD_OPTION = (By.XPATH, "//span[contains(text(),'Credit Card')]")
    PAYMENT_SECTION = (By.ID, "paymentSection")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def select_credit_card(self):
        self.safe_click(self.CREDIT_CARD_OPTION)
        self.logger.info("Selected Credit Card option")

    def validate_payment_section(self):
        section = self.wait_for_element(self.PAYMENT_SECTION)
        assert section.is_displayed(), "Payment section not displayed!"
        self.logger.info("Payment section validated successfully")
