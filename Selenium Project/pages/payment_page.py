import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class PaymentPage(BasePage):
    # PAYMENT TAB LOCATORS
    CREDIT_CARD_TAB = (By.XPATH,
                       "//*[contains(text(), 'Credit & Debit Cards')] | //span[contains(text(), 'Credit & Debit')] | //div[contains(text(), 'Credit & Debit Cards')]")

    # CARD DETAIL FIELD LOCATORS
    CARD_NUMBER_FIELD = (By.XPATH,
                         "//input[contains(@placeholder, 'CARD NUMBER')] | //input[@id='cardNumber'] | //input[contains(@class, 'cardNumber')] | //input[@type='tel' or @name='cardNumber']")
    NAME_ON_CARD_FIELD = (By.XPATH,
                          "//input[contains(translate(@placeholder, 'NAME', 'name'), 'name')] | //input[@id='nameOnCard'] | //input[@name='nameOnCard']")
    CVV_FIELD = (By.XPATH,
                 "//input[@placeholder='CVV'] | //input[@type='password' and contains(@placeholder,'CVV')] | //input[contains(@id,'cvv')] | //input[@name='cvv']")

    # EXPIRY DROPDOWN/INPUT LOCATORS
    EXPIRY_MM_FIELD = (By.XPATH,
                       "//input[@placeholder='MM'] | //div[text()='MM'] | //input[contains(@id,'month')] | //input[@name='expiryMonth']")
    EXPIRY_YY_FIELD = (By.XPATH,
                       "//input[@placeholder='YY'] | //div[text()='YY'] | //input[contains(@id,'year')] | //input[@name='expiryYear']")

    def select_credit_card_option(self):
        logger.info("POM LOG: LOCATING CREDIT/DEBIT CARD PAYMENT TAB")
        try:
            # Hard pause to let the blue AJAX loading spinner finish and the React DOM to stabilize
            time.sleep(5)

            # Now safely grab the stabilized element
            cc_tab = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(self.CREDIT_CARD_TAB)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cc_tab)
            time.sleep(1)

            # Re-fetch the element instantly before clicking to absolutely guarantee it is not stale
            fresh_cc_tab = self.driver.find_element(*self.CREDIT_CARD_TAB)
            self.driver.execute_script("arguments[0].click();", fresh_cc_tab)
            logger.info("POM LOG: CREDIT/DEBIT CARD TAB SELECTED SUCCESSFULLY")
            time.sleep(2)

        except Exception as e:
            logger.error(f"POM LOG: FAILED TO LOCATE OR CLICK CREDIT CARD TAB: {str(e)}")
            raise

    def enter_card_details(self, card_number, expiry, cvv, card_holder):
        logger.info("POM LOG: INITIALIZING CARD DETAILS INJECTION")
        try:
            # 1. Fill Card Number
            card_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.CARD_NUMBER_FIELD)
            )
            card_input.clear()
            # Clean floating points from excel (e.g., 4111.0 -> 4111)
            clean_card = str(int(float(card_number))) if '.' in str(card_number) else str(card_number)
            card_input.send_keys(clean_card)
            logger.info("POM LOG: CARD NUMBER COMMITTED")
            time.sleep(1)

            # 2. Parse Expiry and Fill MM / YY
            month, year = "12", "28"  # Default fallbacks
            if "/" in str(expiry):
                month, year = str(expiry).split("/")

            # Handle MM
            mm_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.EXPIRY_MM_FIELD))
            try:
                mm_input.clear()
                mm_input.send_keys(month.strip())
            except Exception:
                # Fallback if it's a dropdown div instead of an input
                self.driver.execute_script("arguments[0].click();", mm_input)
                time.sleep(1)
                month_opt = self.driver.find_element(By.XPATH,
                                                     f"//li[text()='{month.strip()}'] | //span[text()='{month.strip()}']")
                self.driver.execute_script("arguments[0].click();", month_opt)
            logger.info(f"POM LOG: EXPIRY MONTH COMMITTED -> {month.strip()}")
            time.sleep(0.5)

            # Handle YY
            yy_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.EXPIRY_YY_FIELD))
            try:
                yy_input.clear()
                yy_input.send_keys(year.strip())
            except Exception:
                # Fallback if it's a dropdown div instead of an input
                self.driver.execute_script("arguments[0].click();", yy_input)
                time.sleep(1)
                year_opt = self.driver.find_element(By.XPATH,
                                                    f"//li[text()='{year.strip()}'] | //span[text()='{year.strip()}']")
                self.driver.execute_script("arguments[0].click();", year_opt)
            logger.info(f"POM LOG: EXPIRY YEAR COMMITTED -> {year.strip()}")
            time.sleep(0.5)

            # 3. Fill CVV
            cvv_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.CVV_FIELD))
            cvv_input.clear()
            clean_cvv = str(int(float(cvv))) if '.' in str(cvv) else str(cvv)
            cvv_input.send_keys(clean_cvv)
            logger.info("POM LOG: CVV COMMITTED")
            time.sleep(0.5)

            # 4. Fill Name on Card
            try:
                name_input = self.driver.find_element(*self.NAME_ON_CARD_FIELD)
                name_input.clear()
                name_input.send_keys(str(card_holder))
                logger.info("POM LOG: CARD HOLDER NAME COMMITTED")
                time.sleep(1)
            except Exception:
                logger.info("POM LOG: CARD HOLDER NAME FIELD NOT PRESENT/REQUIRED ON THIS VIEW. SKIPPING.")

            logger.info("POM LOG: ALL DUMMY PAYMENT DETAILS INJECTED SUCCESSFULLY. END OF E2E FLOW REACHED.")
            time.sleep(3)  # Final pause to visually verify fields are filled

        except Exception as e:
            logger.error(f"POM LOG: FAULT OCCURRED WHILE INJECTING CARD DATA: {str(e)}")
            raise