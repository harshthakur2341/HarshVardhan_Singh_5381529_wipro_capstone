from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config_reader import ConfigReader
from utils.logger import LogGen

logger = LogGen.loggen()

class WaitUtils:
    timeout_duration = ConfigReader.get_timeout()

    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=timeout_duration):
        try:
            logger.info(f"Waiting for element visibility : {locator}")
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for visibility : {locator}")
            raise

    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=timeout_duration):
        try:
            logger.info(f"Waiting for element clickable : {locator}")
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for clickable : {locator}")
            raise

    @staticmethod
    def wait_for_presence_of_element(driver, locator, timeout=timeout_duration):
        try:
            logger.info(f"Waiting for element presence : {locator}")
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for presence : {locator}")
            raise