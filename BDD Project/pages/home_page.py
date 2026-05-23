import time

from selenium.common import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.home_locators import HomeLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class HomePage(BasePage):
    def close_popup(self):
        logger.info("POM LOG: Attempting to handle potential login popup modal")
        try:
            time.sleep(2)
            close_btn = self.driver.find_element(*HomeLocators.CLOSE_MODAL_BTN)
            self.driver.execute_script("arguments[0].click();", close_btn)
            logger.info("POM LOG: LOGIN POPUP SUCCESSFULLY CLOSED VIA XPATH CLICK")
            time.sleep(1)
        except Exception as e_close:
            logger.info(f"POM LOG: Native close button unavailable ({str(e_close)}). Attempting body click fallback...")
            try:
                body = self.driver.find_element(*HomeLocators.BODY)
                body.click()
                logger.info("POM LOG: POPUP DISMISSED BY CLICKING OUTSIDE (BODY CLICK)")
                time.sleep(1)
            except Exception as e_body:
                logger.info(f"POM LOG: NO POPUP FOUND OR INTERCEPTED | Message: {str(e_body)}")

    def select_train_tab(self):
        logger.info("POM LOG: Initializing selection of the Trains navigation tab")
        try:
            # FIX 1: Check if we are already on the trains page via the Base URL
            if "railways" in self.driver.current_url:
                return

            # FIX 2: Increased Explicit Wait to 15 seconds to bypass slow-loading overlays
            train_tab = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(HomeLocators.TRAIN_TAB))
            self.driver.execute_script("arguments[0].click();", train_tab)
            logger.info("POM LOG: TRAIN TAB SUCCESSFULLY CLICKED")
            time.sleep(2)
        except Exception as e:
            logger.error(f"POM LOG: FAILED TO INTERACT WITH TRAIN TAB | Exception: {str(e)}")
            raise

    def select_station(self, locator_tuple, station):
        logger.info(f"POM LOG: Attempting to select station: {station}")
        try:
            # 1. Attempt to click the container label
            container = self.wait.until(EC.element_to_be_clickable(locator_tuple))

            try:
                container.click()
            except Exception:
                # If clicking the label fails, the input is likely already active/intercepting
                logger.info("POM LOG: Label click intercepted, attempting direct input interaction.")
                self.driver.execute_script("arguments[0].click();", container)

            # 2. Wait for the active input, clear it, and enter the station
            active_input = self.wait.until(EC.visibility_of_element_located(HomeLocators.ACTIVE_INPUT))
            active_input.clear()
            active_input.send_keys(station)

            # 3. Wait for suggestions
            time.sleep(2)
            first_option = self.wait.until(EC.element_to_be_clickable(HomeLocators.FIRST_SUGGESTION))
            self.driver.execute_script("arguments[0].click();", first_option)

        except Exception as e:
            logger.error(f"POM LOG: Failed to select {station}. Exception: {str(e)}")
            raise

    def select_date(self):
        logger.info("POM LOG: Starting target travel date selection sequence")
        try:
            date_box = self.wait.until(EC.element_to_be_clickable(HomeLocators.DATE_BOX))
            self.driver.execute_script("arguments[0].click();", date_box)
            logger.info("POM LOG: Travel date calendar container expanded")
            time.sleep(2)

            target_date = self.wait.until(EC.element_to_be_clickable(HomeLocators.TARGET_DATE))
            self.driver.execute_script("arguments[0].click();", target_date)
            logger.info("POM LOG: 30 MAY 2026 DATE SELECTION SUBMITTED SUCCESSFULLY")
            time.sleep(2)
        except Exception as e:
            logger.error(f"POM LOG: DATE SELECTION PIPELINE FAILURE | Exception: {str(e)}")
            raise

    def select_class(self):
        logger.info("POM LOG: Initiating Travel Class dropdown selector configuration")
        try:
            # 1. Open the dropdown
            class_box = self.wait.until(EC.element_to_be_clickable(HomeLocators.CLASS_BOX))
            self.driver.execute_script("arguments[0].click();", class_box)
            logger.info("POM LOG: Travel Class dropdown opened")
            time.sleep(2)

            # 2. Select "All Class"
            # We use a standard click here since the element is now visible
            all_class_option = self.wait.until(EC.element_to_be_clickable(HomeLocators.ALL_CLASS))
            all_class_option.click()

            logger.info("POM LOG: ALL CLASS FILTER SELECTED SUCCESSFULLY")
            time.sleep(2)
        except Exception as e:
            logger.error(f"POM LOG: TRAVEL CLASS FILTRATION FAILED | Exception: {str(e)}")
            raise

    def click_search(self):
        logger.info("POM LOG: Dispatching form submission execution via Search Button wrapper link")
        try:
            search_btn = self.wait.until(EC.element_to_be_clickable(HomeLocators.SEARCH_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
            time.sleep(2)
            search_btn.click()
            logger.info("POM LOG: SEARCH ACTION EVENT SENT TO CORE ENGINE SUCCESSFULLY")
            time.sleep(5)
        except Exception as e:
            logger.error(f"POM LOG: SEARCH ACTION DISPATCH FAILURE | Exception: {str(e)}")
            raise

    def search_train(self, from_station, to_station):
        logger.info(
            f"POM LOG: RUNNING HIGH LEVEL COMPOSITE TRAIN SEARCH ROUTINE | From: {from_station} -> To: {to_station}")
        try:
            self.close_popup()
            time.sleep(2)

            logger.info(f"POM LOG: Routing From Station parameter: {from_station}")
            self.select_station(HomeLocators.FROM_FIELD, from_station)

            logger.info(f"POM LOG: Routing To Station parameter: {to_station}")
            self.select_station(HomeLocators.TO_FIELD, to_station)

            self.select_date()
            self.click_search()
            logger.info("POM LOG: COMPOSITE E2E TRAIN SEARCH OPERATION SUCCESSFULLY COMPLETED")
        except Exception as e:
            logger.error(f"POM LOG: CRITICAL ORCHESTRATION PIPELINE ABORTED INSIDE search_train | Exception: {str(e)}")
            raise


    # Add this to your HomePage class
    def get_same_station_error_text(self):
        try:
            # Wait a few seconds for the error to appear
            error_element = self.wait.until(
                EC.visibility_of_element_located(HomeLocators.SAME_STATION_ERROR)
            )
            return error_element.text
        except TimeoutException:
            return None