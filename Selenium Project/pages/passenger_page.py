import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class PassengerPage(BasePage):
    # --- DOM LOCATORS ---
    PAY_FEES_CANCELLATION_RADIO = (By.XPATH, "//label[@for='pay_fees'] | //input[@id='pay_fees']")
    ADD_TRAVELLER_LINK = (By.XPATH,
                          "//div[contains(@class, 'trdSelectTraveller')]//span[text()='Add Traveller']/ancestor::a")

    TRAVELLER_NAME_INPUT = (By.XPATH, "//input[@id='name' or @placeholder='Enter Traveller Name']")
    TRAVELLER_AGE_INPUT = (By.ID, "age")
    GENDER_DROPDOWN_CONTAINER = (By.XPATH, "//div[contains(@class, 'genderField')]//div[@role='button']")
    MODAL_ADD_BTN = (By.XPATH, "//button[contains(@class, 'bluePrimarybtn') and text()='Add']")

    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @placeholder='Email']")
    MOBILE_INPUT = (By.XPATH, "//input[@id='mobileNumber']")

    # Base trigger element for the IRCTC section
    IRCTC_TRIGGER = (By.XPATH, "//input[@id='irctcUserName'] | //div[contains(@class,'irctcSignUp')]")

    def select_cancellation_insurance(self):
        logger.info("POM LOG: TARGETING CANCELLATION PROTECTION RADIO BUTTON")
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.PAY_FEES_CANCELLATION_RADIO)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info("POM LOG: CANCELLATION SELECTION SUCCESSFULLY COMPLETED")
        except Exception as e:
            logger.error(f"POM LOG: CRITICAL FAILURE SELECTING CANCELLATION OPTION: {str(e)}")
            raise

    def open_add_traveller_modal(self):
        logger.info("POM LOG: DISPATCHING CLICK INTERACTION TO ADD TRAVELLER LINK")
        try:
            link = WebDriverWait(self.driver, 25).until(
                EC.visibility_of_element_located(self.ADD_TRAVELLER_LINK)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", link)
            logger.info("POM LOG: ADD TRAVELLER POPUP MODAL INSTANTIATED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"POM LOG: FAILED TO OPEN TRAVELLER DATA ENTRY INTERFACE: {str(e)}")
            raise

    def fill_traveller_details_and_submit(self, name, age, gender, berth_pref=None):
        logger.info(f"POM LOG: FILLING MODAL -> NAME: {name}, AGE: {age}, GENDER: {gender}")
        try:
            time.sleep(2.0)
            name_field = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.TRAVELLER_NAME_INPUT))
            name_field.clear()
            time.sleep(0.2)
            name_field.send_keys(str(name))

            age_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.TRAVELLER_AGE_INPUT))
            age_field.clear()
            time.sleep(0.2)
            age_field.send_keys(str(int(age)))

            gender_dd = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.GENDER_DROPDOWN_CONTAINER))
            gender_dd.click()
            time.sleep(1.0)

            formatted_gender = str(gender).strip().capitalize()
            gender_option_xpath = (
                f"//ul[contains(@class, 'dropdown')]//li[text()='{formatted_gender}'] | "
                f"//div[contains(@class, 'select')]//span[text()='{formatted_gender}'] | "
                f"//li[contains(text(), '{formatted_gender}')]"
            )

            gender_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, gender_option_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", gender_option)
            time.sleep(0.5)

            add_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.MODAL_ADD_BTN))
            self.driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(2.0)
            logger.info("POM LOG: TRAVELLER SUBMITTED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"POM LOG: ERROR ENCOUNTERED PROCESSING MODAL SCHEDULER POPUP: {str(e)}")
            raise

    def fill_contact_details(self, email, mobile):
        logger.info(f"POM LOG: FILLING CONTACT DETAILS -> EMAIL: {email}, MOBILE: {mobile}")
        try:
            email_field = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.EMAIL_INPUT))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_field)
            time.sleep(0.5)
            email_field.clear()
            email_field.send_keys(str(email))

            mobile_field = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.MOBILE_INPUT))
            mobile_field.clear()
            time.sleep(0.2)
            mobile_field.send_keys(str(mobile))
            logger.info("POM LOG: CONTACT DETAILS POPULATED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"POM LOG: FAILED TO POPULATE CONTACT DETAILS: {str(e)}")
            raise

    def enter_irctc_id(self, irctc_id):
        logger.info(f"POM LOG: INITIATING IRCTC USERNAME OVERLAY SELECTION FOR: {irctc_id}")
        try:
            # 1. Target the trigger field/container on the page
            trigger_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.IRCTC_TRIGGER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger_field)
            time.sleep(0.5)

            # Check if the modal overlay is already present before trying to click
            modal_check = self.driver.find_elements(By.ID, "mmt-irctc-modal")

            if not modal_check:
                logger.info("POM LOG: Modal not detected. Forcing click on IRCTC trigger via JavaScript.")
                self.driver.execute_script("arguments[0].click();", trigger_field)
                time.sleep(2.0)  # Wait for the overlay transition animations
            else:
                logger.info("POM LOG: IRCTC Modal overlay already active on DOM. Proceeding directly to entry.")

            # 2. Extract the actual user input fields present inside the active modal frame
            inputs = self.driver.find_elements(By.XPATH, "//div[@id='mmt-irctc-modal']//input[@id='irctcUserName']")
            if not inputs:
                inputs = self.driver.find_elements(By.XPATH, "//div[@id='mmt-irctc-modal']//input")

            if not inputs:
                raise Exception("CRITICAL: IRCTC text input element could not be found within the modal context.")

            # Grab the last element in the list (the active interactive overlay layout layer)
            modal_input = inputs[-1]

            # === NEW: EXPLICITLY CLICK THE POPUP INPUT FIELD ===
            logger.info("POM LOG: Clicking explicitly inside the IRCTC username popup input field.")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(modal_input))
            modal_input.click()
            time.sleep(0.5)

            # Flush existing front-end values completely
            self.driver.execute_script("arguments[0].value = '';", modal_input)
            modal_input.clear()
            time.sleep(0.3)

            # Send the data payload keys
            modal_input.send_keys(str(irctc_id))
            logger.info("POM LOG: IRCTC ID TYPED SUCCESSFULLY INTO ACTIVE MODAL INPUT LAYER")
            time.sleep(1.5)  # Let React state updates finalize (enables the submit button)

            # 3. Locate the submit confirmation buttons directly nested inside the modal context container
            submit_buttons = self.driver.find_elements(By.XPATH,
                                                       "//div[@id='mmt-irctc-modal']//button[contains(., 'Submit') or contains(., 'SUBMIT')]")
            if not submit_buttons:
                submit_buttons = self.driver.find_elements(By.XPATH,
                                                           "//button[contains(., 'Submit') or contains(., 'SUBMIT')]")

            if not submit_buttons:
                raise Exception("CRITICAL: Target Submit option button not found inside page layout.")

            modal_submit = submit_buttons[-1]

            # Wait for button lifecycle validation states to clear up
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(modal_submit))

            # Execute final submit via JavaScript click to guarantee bypass of any lingering overlay blocks
            self.driver.execute_script("arguments[0].click();", modal_submit)
            time.sleep(2.5)
            logger.info("POM LOG: IRCTC ID SUBMITTED VIA MODAL EXECUTION")

        except Exception as e:
            logger.error(f"POM LOG: FAILURE ENCOUNTERED RUNNING IRCTC PROMPT: {str(e)}")
            raise

    def click_mandatory_checkbox(self):
        logger.info("POM LOG: Targeting the mandatory confirmation checkbox wrapper.")
        try:
            # Locator based on the unique data-cy attribute found in image_3f74ce.png
            checkbox_locator = (By.XPATH,
                                "//div[@data-cy='dt_cb_input_gst_info'] | //div[contains(@class, 'checkboxWithLblWpr')]")

            checkbox_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(checkbox_locator)
            )

            # Scroll to center the checkbox frame cleanly on screen
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_element)
            time.sleep(0.5)

            # Click it cleanly using JavaScript to avoid background overlay clashes
            self.driver.execute_script("arguments[0].click();", checkbox_element)
            logger.info("POM LOG: Mandatory checkbox successfully marked.")
            time.sleep(1.0)

        except Exception as e:
            logger.error(f"POM LOG: Failed to click mandatory checkbox: {str(e)}")
            raise

    def click_pay_and_book_now(self):
        logger.info("POM LOG: Targeting the 'PAY & BOOK NOW' button anchor link.")
        try:
            # Locator targeting the specific payment button classes shown in image_3f78af.png
            pay_button_locator = (By.XPATH, "//a[contains(@class, 'paymentBtn') or contains(., 'PAY & BOOK NOW')]")

            pay_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(pay_button_locator)
            )

            # Ensure it is clearly visible in the browser viewport window frame
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pay_button)
            time.sleep(0.5)

            # Execute the click hook event
            self.driver.execute_script("arguments[0].click();", pay_button)
            logger.info("POM LOG: 'PAY & BOOK NOW' action dispatched successfully.")

        except Exception as e:
            logger.error(f"POM LOG: Failed to execute PAY & BOOK NOW selection: {str(e)}")
            raise