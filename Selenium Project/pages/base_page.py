import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class BasePage:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 20)

    def wait_for_element(self, locator):
        self.logger.info(f"Waiting for element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        self.logger.info(f"Waiting for clickable element: {locator}")
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        try:
            element = self.wait_for_clickable(locator)
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Click failed: {locator}, retrying with JS click")
            self.js_click(locator)

    def js_click(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"JS clicked element: {locator}")

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Typed '{text}' into element: {locator}")

    def get_text(self, locator):
        element = self.wait_for_element(locator)
        text = element.text
        self.logger.info(f"Got text '{text}' from element: {locator}")
        return text

    def scroll_to_element(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")

    def hover(self, locator):
        element = self.wait_for_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")

    def select_dropdown(self, locator, value):
        from selenium.webdriver.support.ui import Select
        element = self.wait_for_element(locator)
        Select(element).select_by_visible_text(value)
        self.logger.info(f"Selected '{value}' from dropdown: {locator}")

    def safe_send_keys(self, locator, text):
        try:
            self.type(locator, text)
        except Exception as e:
            self.logger.error(f"Send keys failed for {locator}, retrying...")
            time.sleep(2)
            self.type(locator, text)

    def safe_click(self, locator):
        try:
            self.click(locator)
        except Exception as e:
            self.logger.error(f"Safe click failed for {locator}, retrying...")
            time.sleep(2)
            self.js_click(locator)

    def take_screenshot(self, name):
        path = f"screenshots/{name}.png"
        self.driver.save_screenshot(path)
        self.logger.info(f"Screenshot saved: {path}")
        return path
