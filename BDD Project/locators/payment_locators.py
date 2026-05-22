from selenium.webdriver.common.by import By

class PaymentLocators:
    CREDIT_CARD_TAB = (By.XPATH, "//*[contains(text(), 'Credit & Debit Cards')] | //span[contains(text(), 'Credit & Debit')] | //div[contains(text(), 'Credit & Debit Cards')]")
    CARD_NUMBER_FIELD = (By.XPATH, "//input[contains(@placeholder, 'CARD NUMBER')] | //input[@id='cardNumber'] | //input[contains(@class, 'cardNumber')] | //input[@type='tel' or @name='cardNumber']")
    NAME_ON_CARD_FIELD = (By.XPATH, "//input[contains(translate(@placeholder, 'NAME', 'name'), 'name')] | //input[@id='nameOnCard'] | //input[@name='nameOnCard']")
    CVV_FIELD = (By.XPATH, "//input[@placeholder='CVV'] | //input[@type='password' and contains(@placeholder,'CVV')] | //input[contains(@id,'cvv')] | //input[@name='cvv']")
    EXPIRY_MM_FIELD = (By.XPATH, "//input[@placeholder='MM'] | //div[text()='MM'] | //input[contains(@id,'month')] | //input[@name='expiryMonth']")
    EXPIRY_YY_FIELD = (By.XPATH, "//input[@placeholder='YY'] | //div[text()='YY'] | //input[contains(@id,'year')] | //input[@name='expiryYear']")

    PAYMENT_CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='continue']")