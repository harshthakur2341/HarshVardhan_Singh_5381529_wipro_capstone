from selenium.webdriver.common.by import By


class PassengerLocators:
    TRAIN_DETAILS_LOADED = (By.CLASS_NAME, "railTravellersContainer")

    TRAIN_DETAILS_HEADER = (By.XPATH, "//div[contains(@class,'train-details-header')]")
    PAY_FEES_CANCELLATION_RADIO = (By.XPATH, "//label[@for='pay_fees'] | //input[@id='pay_fees']")
    ADD_TRAVELLER_LINK = (By.XPATH,
                          "//div[contains(@class, 'trdSelectTraveller')]//span[text()='Add Traveller']/ancestor::a")
    TRAVELLER_NAME_INPUT = (By.XPATH, "//input[@id='name' or @placeholder='Enter Traveller Name']")
    TRAVELLER_AGE_INPUT = (By.ID, "age")
    GENDER_DROPDOWN_CONTAINER = (By.XPATH, "//div[contains(@class, 'genderField')]//div[@role='button']")
    MODAL_ADD_BTN = (By.XPATH, "//button[contains(@class, 'bluePrimarybtn') and text()='Add']")

    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @placeholder='Email']")
    #MOBILE_INPUT = (By.XPATH, "//input[@id='mobileNumber']")
    MOBILE_INPUT = (By.NAME, "Mobile Number")

    IRCTC_TRIGGER = (By.XPATH, "//input[@id='irctcUserName'] | //div[contains(@class,'irctcSignUp')]")
    IRCTC_MODAL_CHECK = (By.ID, "mmt-irctc-modal")
    IRCTC_MODAL_INPUT = (By.XPATH, "//div[@id='mmt-irctc-modal']//input[@id='irctcUserName']")
    IRCTC_MODAL_INPUT_FALLBACK = (By.XPATH, "//div[@id='mmt-irctc-modal']//input")
    IRCTC_MODAL_SUBMIT = (By.XPATH,
                          "//div[@id='mmt-irctc-modal']//button[contains(., 'Submit') or contains(., 'SUBMIT')]")
    IRCTC_SUBMIT_FALLBACK = (By.XPATH, "//button[contains(., 'Submit') or contains(., 'SUBMIT')]")

    MANDATORY_CHECKBOX = (By.XPATH,
                          "//div[@data-cy='dt_cb_input_gst_info'] | //div[contains(@class, 'checkboxWithLblWpr')]")
    PAY_BUTTON = (By.XPATH, "//a[contains(@class, 'paymentBtn') or contains(., 'PAY & BOOK NOW')]")


    @staticmethod
    def get_dynamic_gender_locator(gender):
        formatted_gender = str(gender).strip().capitalize()
        xpath = (
                f"//ul[contains(@class, 'dropdown')]//li[text()='{formatted_gender}'] | "
                f"//div[contains(@class, 'select')]//span[text()='{formatted_gender}'] | "
                f"//li[contains(text(), '{formatted_gender}')]"
            )
        return (By.XPATH, xpath)