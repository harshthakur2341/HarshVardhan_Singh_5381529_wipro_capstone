import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NavigationHandler:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 20)
        self.main_window = driver.current_window_handle

    def wait_for_page_load(self):
        self.logger.info("Waiting for page load completion...")
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def wait_for_url_contains(self, text):
        self.logger.info(f"Waiting for URL to contain: {text}")
        self.wait.until(EC.url_contains(text))

    def switch_to_new_window(self):
        self.logger.info("Switching to new window...")
        time.sleep(2)
        for handle in self.driver.window_handles:
            if handle != self.main_window:
                self.driver.switch_to.window(handle)
                self.logger.info("Switched to new window")
                break

    def switch_to_main_window(self):
        self.driver.switch_to.window(self.main_window)
        self.logger.info("Switched back to main window")

    def handle_page_transition(self, expected_url_fragment):
        self.logger.info(f"Handling page transition to: {expected_url_fragment}")
        self.wait_for_page_load()
        self.wait_for_url_contains(expected_url_fragment)

    def retry_element(self, locator, retries=3):
        for attempt in range(retries):
            try:
                element = self.driver.find_element(*locator)
                self.logger.info(f"Element found on attempt {attempt+1}: {locator}")
                return element
            except Exception as e:
                self.logger.warning(f"Retry {attempt+1} failed for {locator}, retrying...")
                time.sleep(2)
        self.logger.error(f"Element not found after {retries} retries: {locator}")
        return None

    def safe_click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked element safely: {locator}")
        except Exception as e:
            self.logger.error(f"Safe click failed: {locator}, retrying with JS click")
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
