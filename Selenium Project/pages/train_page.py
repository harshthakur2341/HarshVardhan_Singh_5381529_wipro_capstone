from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.navigation import NavigationHandler

class TrainPage(BasePage):
    FROM_INPUT = (By.ID, "fromCity")
    TO_INPUT = (By.ID, "toCity")
    DATE_INPUT = (By.ID, "travelDate")
    CLASS_DROPDOWN = (By.ID, "trainClass")
    SEARCH_BTN = (By.XPATH, "//button[contains(text(),'Search')]")
    TRAIN_SELECT_BTN = (By.XPATH, "//button[contains(text(),'Book Now')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.nav_handler = NavigationHandler(driver, logger)

    def search_train(self, from_station, to_station, travel_date, train_class):
        self.safe_send_keys(self.FROM_INPUT, from_station)
        self.safe_send_keys(self.TO_INPUT, to_station)
        self.safe_send_keys(self.DATE_INPUT, travel_date)
        self.select_dropdown(self.CLASS_DROPDOWN, train_class)
        self.safe_click(self.SEARCH_BTN)
        self.nav_handler.handle_page_transition("railways/listing")
        self.logger.info("Train search executed")

    def select_train(self):
        self.safe_click(self.TRAIN_SELECT_BTN)
        self.nav_handler.handle_page_transition("railways/passenger")
        self.logger.info("Train selected, navigating to Passenger page")
