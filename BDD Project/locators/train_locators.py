from selenium.webdriver.common.by import By

class TrainLocators:
    TRAIN_RESULTS_HEADER = (By.XPATH, "//*[contains(text(), 'trains found')]")
    AC_FILTER_BTN = (By.XPATH, "//label[@data-testid='filter-ac'] | //label[@for='AC']")
    AVAILABLE_FILTER_BTN = (By.XPATH, "//label[@data-testid='filter-available'] | //label[@for='Available']")
    FIRST_AVAILABLE_TRAIN_BTN = (By.XPATH, "(//div[@data-testid='card-wrapper'])[1]//*[contains(text(), 'Available') or contains(text(), 'AVAILABLE')]")