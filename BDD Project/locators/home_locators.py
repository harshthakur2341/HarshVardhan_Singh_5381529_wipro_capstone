from selenium.webdriver.common.by import By


class HomeLocators:
    CLOSE_MODAL_BTN = (By.XPATH, "//span[@data-cy='closeModal']")
    BODY = (By.TAG_NAME, "body")
    TRAIN_TAB = (By.XPATH, "//span[contains(text(),'Trains')]")
    ACTIVE_INPUT = (By.XPATH, "//input[contains(@placeholder,'From') or contains(@placeholder,'To')]")
    FIRST_SUGGESTION = (By.XPATH, "(//ul[contains(@class,'react-autosuggest')]//li)[1]")
    DATE_BOX = (By.XPATH, "//label[@for='travelDate']")
    TARGET_DATE = (By.XPATH, "//div[@aria-label='Sat May 30 2026']")
    CLASS_BOX = (By.XPATH, "//span[contains(text(),'Class')]")
    ALL_CLASS = (By.XPATH, "//li[@data-cy='ALL']")
    SEARCH_BTN = (By.XPATH, "//a[contains(text(),'Search')]")

    FROM_FIELD = (By.XPATH, "//label[@for='fromCity']")
    TO_FIELD = (By.XPATH, "//label[@for='toCity']")