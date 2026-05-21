import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class TrainPage(BasePage):

    TRAIN_RESULTS_HEADER = (By.XPATH, "//*[contains(text(), 'trains found')]")

    # FILTER LOCATORS
    AC_FILTER_BTN = (By.XPATH, "//label[@data-testid='filter-ac'] | //label[@for='AC']")
    AVAILABLE_FILTER_BTN = (By.XPATH, "//label[@data-testid='filter-available'] | //label[@for='Available']")

    # FIXED LOCATOR: Targets the actual text element showing availability inside the first train card wrapper
    FIRST_AVAILABLE_TRAIN_BTN = (By.XPATH,
                                 "(//div[@data-testid='card-wrapper'])[1]//*[contains(text(), 'Available') or contains(text(), 'AVAILABLE')]")

    def verify_train_search_result(self):
        logger.info("POM LOG: VERIFYING TRAIN SEARCH RESULTS PAGE")
        WebDriverWait(self.driver, 45).until(
            EC.url_contains("railways/listing")
        )
        time.sleep(2)
        WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located(self.TRAIN_RESULTS_HEADER)
        )
        logger.info("POM LOG: TRAIN SEARCH RESULTS CONTAINER VALIDATED")

    def filter_ac_trains(self):
        logger.info("POM LOG: APPLYING AC FILTER")
        try:
            ac_btn = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(self.AC_FILTER_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ac_btn)
            time.sleep(1)
            try:
                ac_btn.click()
                logger.info("POM LOG: AC FILTER DEPLOYED NATIVELY")
            except Exception:
                self.driver.execute_script("arguments[0].click();", ac_btn)
                logger.info("POM LOG: AC FILTER DEPLOYED VIA JS FALLBACK")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: AC FILTER ACTION INTERRUPTED: {str(e)}")
            raise

    def filter_available_trains(self):
        logger.info("POM LOG: APPLYING AVAILABILITY FILTER")
        try:
            avail_btn = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(self.AVAILABLE_FILTER_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", avail_btn)
            time.sleep(1)
            try:
                avail_btn.click()
                logger.info("POM LOG: AVAILABILITY FILTER DEPLOYED NATIVELY")
            except Exception:
                self.driver.execute_script("arguments[0].click();", avail_btn)
                logger.info("POM LOG: AVAILABILITY FILTER DEPLOYED VIA JS FALLBACK")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: AVAILABILITY FILTER ACTION INTERRUPTED: {str(e)}")
            raise

    def select_first_available_train_ticket(self):
        logger.info("POM LOG: SELECTING FIRST AVAILABLE TRAIN SEAT OPTION")
        try:
            time.sleep(3)  # Wait for filters to finish re-rendering the cards

            # 1. Locate the availability text element
            btn = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(self.FIRST_AVAILABLE_TRAIN_BTN)
            )

            # 2. VERIFICATION STEP: Extract and log the text of what Selenium found
            element_text = btn.text or btn.get_attribute("innerText")
            logger.info(f"POM LOG: VERIFYING TARGET ELEMENT TEXT ---> '{element_text}'")

            # 3. Scroll it to center smoothly
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(1.5)

            # 4. Click the exact element text
            try:
                btn.click()
                logger.info("POM LOG: NATIVE CLICK SENT TO AVAILABILITY TEXT ELEMENT")
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
                logger.info("POM LOG: JS FALLBACK CLICK SENT TO AVAILABILITY TEXT ELEMENT")

            time.sleep(5)  # Give it time to load the traveller details page or open a new window

            # 5. AUTOMATIC WINDOW HANDLING: If MMT opens the passenger details in a new tab, switch to it
            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                logger.info("POM LOG: NEW TAB DETECTED! SWITCHING FOCUS TO PASSENGER DETAILS TAB")
                self.driver.switch_to.window(window_handles[-1])
                logger.info(f"POM LOG: CURRENT URL AFTER SWITCH: {self.driver.current_url}")

        except Exception as e:
            logger.error(f"POM LOG: FAULT INSIDE TRAIN SELECTION PIPELINE: {str(e)}")
            raise

    def apply_ac_filter(self):
        self.filter_ac_trains()

    def apply_available_filter(self):
        self.filter_available_trains()

