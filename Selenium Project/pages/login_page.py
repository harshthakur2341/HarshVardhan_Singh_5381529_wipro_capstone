import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    LOGIN_POPUP = (By.XPATH, "//div[contains(@class,'loginModal')]")
    MOBILE_INPUT = (By.XPATH, "//input[@placeholder='Enter Mobile Number']")
    CONTINUE_BTN = (By.XPATH, "//button[contains(text(),'Continue')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def handle_login_popup(self, mobile_number):
        try:
            popup = self.wait_for_element(self.LOGIN_POPUP)
            if popup.is_displayed():
                self.logger.info("Login popup detected")
                self.safe_send_keys(self.MOBILE_INPUT, mobile_number)
                self.safe_click(self.CONTINUE_BTN)
                self.logger.info("Submitted mobile number for OTP")
                time.sleep(20)  # manual wait for OTP
        except Exception as e:
            self.logger.warning("Login popup not found or already handled")
