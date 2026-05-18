from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.navigation import NavigationHandler

class PassengerPage(BasePage):
    IRCTC_INPUT = (By.ID, "irctcUserId")
    NAME_INPUT = (By.ID, "passengerName")
    AGE_INPUT = (By.ID, "passengerAge")
    GENDER_DROPDOWN = (By.ID, "passengerGender")
    BERTH_DROPDOWN = (By.ID, "berthPreference")
    MOBILE_INPUT = (By.ID, "mobileNumber")
    EMAIL_INPUT = (By.ID, "email")
    CONTINUE_BTN = (By.XPATH, "//button[contains(text(),'Continue')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.nav_handler = NavigationHandler(driver, logger)

    def enter_irctc_id(self, irctc_id):
        self.safe_send_keys(self.IRCTC_INPUT, irctc_id)
        self.logger.info(f"Entered IRCTC ID: {irctc_id}")

    def fill_passenger_details(self, name, age, gender, berth, mobile, email):
        self.safe_send_keys(self.NAME_INPUT, name)
        self.safe_send_keys(self.AGE_INPUT, age)
        self.select_dropdown(self.GENDER_DROPDOWN, gender)
        self.select_dropdown(self.BERTH_DROPDOWN, berth)
        self.safe_send_keys(self.MOBILE_INPUT, mobile)
        self.safe_send_keys(self.EMAIL_INPUT, email)
        self.logger.info(f"Passenger details entered for {name}")

    def continue_booking(self):
        self.safe_click(self.CONTINUE_BTN)
        self.nav_handler.handle_page_transition("railways/review")
        self.logger.info("Navigated to Review Booking page")
