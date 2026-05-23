import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.train_locators import TrainLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class TrainPage(BasePage):
    def verify_train_search_result(self):
        logger.info("POM LOG: Initializing Train Search Results structural verification sequence")
        try:
            WebDriverWait(self.driver, 45).until(EC.url_contains("railways/listing"))
            time.sleep(2)
            WebDriverWait(self.driver, 45).until(EC.presence_of_element_located(TrainLocators.TRAIN_RESULTS_HEADER))
            logger.info("POM LOG: TRAIN SEARCH RESULTS CONTENT FRAMES SUCCESSFULLY VALIDATED AND STABILIZED")
        except Exception as e:
            logger.error(f"POM LOG: TRAIN LISTING RESULTS ROUTE FAILED STRUCTURAL VERIFICATION | Exception: {str(e)}")
            raise

    def filter_ac_trains(self):
        logger.info("POM LOG: Dispatching interaction requests for Air Conditioning (AC) class layout filter")
        try:
            ac_btn = WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable(TrainLocators.AC_FILTER_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ac_btn)
            time.sleep(1)
            try:
                ac_btn.click()
                logger.info("POM LOG: AC FILTER CONFIRMED VIA NATIVE ELEMENT POINTER CLICK ACTION")
            except Exception:
                self.driver.execute_script("arguments[0].click();", ac_btn)
                logger.info("POM LOG: AC FILTER CONFIRMED VIA JAVASCRIPT EXECUTOR BACKUP HOOK")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: AC TRAIN FILTRATION PIPELINE ENCOUNTERED CRITICAL ERROR | Exception: {str(e)}")
            raise

    def filter_available_trains(self):
        logger.info("POM LOG: Dispatching interaction requests for Seat Availability state verification filters")
        try:
            avail_btn = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(TrainLocators.AVAILABLE_FILTER_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", avail_btn)
            time.sleep(1)
            try:
                avail_btn.click()
                logger.info("POM LOG: AVAILABILITY FILTER CONFIRMED VIA NATIVE ELEMENT POINTER CLICK ACTION")
            except Exception:
                self.driver.execute_script("arguments[0].click();", avail_btn)
                logger.info("POM LOG: AVAILABILITY FILTER CONFIRMED VIA JAVASCRIPT EXECUTOR BACKUP HOOK")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: SEAT AVAILABILITY TRAIN FILTRATION PIPELINE INTERRUPTED | Exception: {str(e)}")
            raise

    def select_first_available_train_ticket(self):
        logger.info("POM LOG: Parsing layout map structures to intercept first available active inventory card element")
        try:
            time.sleep(3)
            btn = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(TrainLocators.FIRST_AVAILABLE_TRAIN_BTN))
            element_text = btn.text or btn.get_attribute("innerText")
            logger.info(
                f"POM LOG: ELEMENT STRING TARGET VALUE VERIFICATION COMPLETED ---> Content payload read: '{element_text}'")

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(1.5)

            try:
                btn.click()
                logger.info("POM LOG: TICKET INVENTORY INTERACTION LINK RESOLVED VIA NATIVE CLICK MAPPING")
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
                logger.info("POM LOG: TICKET INVENTORY INTERACTION LINK RESOLVED VIA JS FALLBACK INJECTION")

            time.sleep(5)

            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                logger.info(
                    f"POM LOG: MULTI-WINDOW STATE DETECTED! Context arrays match length count: {len(window_handles)}")
                self.driver.switch_to.window(window_handles[-1])
                logger.info(f"POM LOG: CONTEXT TARGET FOCUS SWITCHED TO WORKSTATION URL: {self.driver.current_url}")
        except Exception as e:
            logger.error(f"POM LOG: FAULT DETECTED TERMINATING INVENTORY SELECTION PROCESSING | Exception: {str(e)}")
            raise

    def apply_ac_filter(self):
        logger.info("POM LOG: Executing short-circuit alias method call -> apply_ac_filter")
        try:
            self.filter_ac_trains()
        except Exception as e:
            logger.error(f"POM LOG: Shortcut execution failed inside apply_ac_filter wrap | Exception: {str(e)}")
            raise

    def apply_available_filter(self):
        logger.info("POM LOG: Executing short-circuit alias method call -> apply_available_filter")
        try:
            self.filter_available_trains()
        except Exception as e:
            logger.error(f"POM LOG: Shortcut execution failed inside apply_available_filter wrap | Exception: {str(e)}")
            raise