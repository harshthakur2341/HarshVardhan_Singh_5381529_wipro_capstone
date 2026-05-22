import time

from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.passenger_locators import PassengerLocators
from utils.logger import LogGen

logger = LogGen.loggen()

class PassengerPage(BasePage):
    def select_cancellation_insurance(self):
        logger.info("POM LOG: Initializing location verification routines for zero-fee booking cancellation insurance option mapping")
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(PassengerLocators.PAY_FEES_CANCELLATION_RADIO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info("POM LOG: BOOKING PROTECTION FEE SELECTION PACKETS RESOLVED AND MARKED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"POM LOG: SELECTION SEQUENCE ABORTED ON CANCELLATION OPTION WRAPPER FIELD | Exception: {str(e)}")
            raise

    def open_add_traveller_modal(self):
        logger.info("POM LOG: Preparing workspace interface parameters to dispatch interactive link for 'Add Traveller' trigger link")
        try:
            link = WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located(PassengerLocators.ADD_TRAVELLER_LINK))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", link)
            logger.info("POM LOG: NEW MODAL FRAME SCHEDULER LAYOUT DISPATCHED AND DETECTED IN WEBVIEW VIEWPORT")
        except Exception as e:
            logger.error(f"POM LOG: FAILED TO MOUNT SYSTEM DIALOG DRAWER OVERLAY OVER COMPONENT ELEMENT | Exception: {str(e)}")
            raise

    def fill_traveller_details_and_submit(self, name, age, gender, berth_pref=None):
        logger.info(
            f"POM LOG: Injecting passenger profile data matrices -> Data payload maps: [NAME: {name} | AGE: {age} | GENDER: {gender}]")
        try:
            time.sleep(2.0)

            # 1. Populate Name Field
            name_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(PassengerLocators.TRAVELLER_NAME_INPUT))
            name_field.clear()
            time.sleep(0.2)
            name_field.send_keys(str(name))
            logger.info("POM LOG: Successfully entered passenger name")

            # 2. Populate Age Field
            age_field = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(PassengerLocators.TRAVELLER_AGE_INPUT))
            age_field.clear()
            time.sleep(0.2)
            age_field.send_keys(str(int(age)))
            logger.info("POM LOG: Successfully entered passenger age")

            # 3. Open Gender Dropdown Menu
            gender_dd = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(PassengerLocators.GENDER_DROPDOWN_CONTAINER))
            gender_dd.click()
            time.sleep(1.0)
            logger.info("POM LOG: Gender dropdown expanded")

            # 4. Fetch and click the dynamic gender locator from PassengerLocators
            gender_locator = PassengerLocators.get_dynamic_gender_locator(gender)
            gender_option = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(gender_locator))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_option)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", gender_option)
            logger.info(f"POM LOG: Successfully selected gender option: {gender}")
            time.sleep(0.5)

            # 5. Click the Add Button to submit the modal form
            add_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(PassengerLocators.MODAL_ADD_BTN))
            self.driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(2.0)

            logger.info("POM LOG: MODAL WORKSPACE FORM DATA SUBMITTED AND RETAINED IN COMPONENT CONTEXT SYSTEM")
        except Exception as e:
            logger.error(
                f"POM LOG: SUBMISSION FAILURE DETECTED WHILE INJECTING MODAL DIALOG CONTAINER PAYLOAD | Exception: {str(e)}")
            raise

    def fill_contact_details(self, email, mobile):
        logger.info(
            f"POM LOG: Loading network input values for identity metadata entries -> [EMAIL: {email} | MOBILE: {mobile}]")
        try:
            # 1. Handle Email Field
            email_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(PassengerLocators.EMAIL_INPUT))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_field)
            time.sleep(0.5)
            email_field.clear()
            email_field.send_keys(str(email))
            # Trigger input event for email
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                       email_field)

            # 2. Handle Mobile Field
            mobile_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(PassengerLocators.MOBILE_INPUT))
            mobile_field.clear()
            time.sleep(0.2)
            mobile_field.send_keys(str(mobile))

            # CRITICAL: Force validation by triggering events and sending a TAB key
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                       mobile_field)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                                       mobile_field)
            mobile_field.send_keys(Keys.TAB)

            logger.info("POM LOG: CONTACT SPECIFIC FIELDS COMMITTED TO FRONTEND STORAGE MATRIX SUCCESSFULLY")
        except Exception as e:
            logger.error(
                f"POM LOG: ENCOUNTERED INJECTION FAILURE ON CONTACT DETAIL INPUT ELEMENTS | Exception: {str(e)}")
            raise

    def enter_irctc_id(self, irctc_id):
        logger.info(f"POM LOG: Processing configuration layouts to resolve IRCTC Identity verification values for: {irctc_id}")
        try:
            trigger_field = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(PassengerLocators.IRCTC_TRIGGER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger_field)
            time.sleep(0.5)

            modal_check = self.driver.find_elements(*PassengerLocators.IRCTC_MODAL_CHECK)

            if not modal_check:
                logger.info("POM LOG: Focus verification layer missing modal elements. Injecting forced execution click on trigger selector frame.")
                self.driver.execute_script("arguments[0].click();", trigger_field)
                time.sleep(2.0)
            else:
                logger.info("POM LOG: Verification layer confirmed modal frame states are active. Skipping initialization click triggers.")

            inputs = self.driver.find_elements(*PassengerLocators.IRCTC_MODAL_INPUT)
            if not inputs:
                inputs = self.driver.find_elements(*PassengerLocators.IRCTC_MODAL_INPUT_FALLBACK)

            if not inputs:
                raise Exception("CRITICAL ERROR: Active context text inputs could not be indexed in operational modal layout frames.")

            modal_input = inputs[-1]
            logger.info("POM LOG: Resolving focusing events natively onto selected target input frames inside system layers")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(modal_input))
            modal_input.click()
            time.sleep(0.5)

            self.driver.execute_script("arguments[0].value = '';", modal_input)
            modal_input.clear()
            time.sleep(0.3)
            modal_input.send_keys(str(irctc_id))
            logger.info("POM LOG: DATA CHARACTERS COMMITTED IN MODAL BUFFER STACKS SUCCESSFULLY")
            time.sleep(1.5)

            submit_buttons = self.driver.find_elements(*PassengerLocators.IRCTC_MODAL_SUBMIT)
            if not submit_buttons:
                submit_buttons = self.driver.find_elements(*PassengerLocators.IRCTC_SUBMIT_FALLBACK)

            if not submit_buttons:
                raise Exception("CRITICAL ERROR: Structural navigation buttons corresponding to submit actions are unindexed.")

            modal_submit = submit_buttons[-1]
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(modal_submit))
            self.driver.execute_script("arguments[0].click();", modal_submit)
            time.sleep(2.5)
            logger.info("POM LOG: IDENTITY MODAL CONTEXT SUBMITTED TO BACKEND CONTROLLER LAYER")
        except Exception as e:
            logger.error(f"POM LOG: ENCOUNTERED EXECUTION EXCEPTIONS WRITING CREDENTIAL RECORDS INSIDE DIALOGS | Exception: {str(e)}")
            raise

    def click_mandatory_checkbox(self):
        logger.info("POM LOG: Validating legal Terms and Confirmation compliance components")
        try:
            checkbox_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(PassengerLocators.MANDATORY_CHECKBOX))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox_element)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", checkbox_element)
            logger.info("POM LOG: COMPLIANCE CHECKBOX VALIDATED AND MARKED TRUE")
            time.sleep(1.0)
        except Exception as e:
            logger.error(f"POM LOG: UNABLE TO VALIDATE REQUISITE STRUCTURAL CHECKBOX FORM ELEMENTS | Exception: {str(e)}")
            raise

    def click_pay_and_book_now(self):
        logger.info("POM LOG: Routing data validation sets to locate final form submission checkout link action elements")
        try:
            pay_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(PassengerLocators.PAY_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pay_button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", pay_button)
            logger.info("POM LOG: PRIMARY CHECKOUT INTENT FORWARDED UNTO SETTLEMENT ENGINE GATEWAYS")
        except Exception as e:
            logger.error(f"POM LOG: PIPELINE CRASHED ATTEMPTING INTERACTION ROUTING WITH PAY BUTTON ROOT LINKS | Exception: {str(e)}")
            raise