from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.navigation import NavigationHandler

class HomePage(BasePage):
    TRAINS_TAB = (By.XPATH, "//span[text()='Trains']")
    BOOK_TRAIN_BTN = (By.XPATH, "//a[contains(text(),'Book Train Tickets')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.nav_handler = NavigationHandler(driver, logger)

    def open_trains_tab(self):
        self.safe_click(self.TRAINS_TAB)
        self.logger.info("Opened Trains tab")

    def click_book_train(self):
        self.safe_click(self.BOOK_TRAIN_BTN)
        self.nav_handler.handle_page_transition("railways/listing")
        self.logger.info("Navigated to Train Listing page")
