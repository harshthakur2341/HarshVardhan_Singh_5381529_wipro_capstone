from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import LogGen

logger = LogGen.loggen()

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        logger.info("POM LOG: BasePage initialized")

    def click(self, locator):
        logger.info(f"POM LOG: Clicking on locator: {locator}")
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            logger.info(f"POM LOG: Successfully clicked on locator: {locator}")
        except Exception as e:
            logger.error(f"POM LOG: Failed to click on locator: {locator} | Exception: {str(e)}")
            raise

    def type(self, locator, text):
        logger.info(f"POM LOG: Typing '{text}' into locator: {locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            logger.info(f"POM LOG: Successfully typed into locator: {locator}")
        except Exception as e:
            logger.error(f"POM LOG: Failed to type into locator: {locator} | Exception: {str(e)}")
            raise

    def get_text(self, locator):
        logger.info(f"POM LOG: Getting text from locator: {locator}")
        try:
            text = self.wait.until(EC.visibility_of_element_located(locator)).text
            logger.info(f"POM LOG: Successfully got text '{text}' from locator: {locator}")
            return text
        except Exception as e:
            logger.error(f"POM LOG: Failed to get text from locator: {locator} | Exception: {str(e)}")
            raise