
import os
from behave import given, when, then

from locators.passenger_locators import PassengerLocators
from locators.payment_locators import PaymentLocators
from utils.logger import LogGen
from utils.excel_reader import ExcelReader
from locators.home_locators import HomeLocators

logger = LogGen.loggen()

# SETUP

@given('User launches MakeMyTrip application')
def step_impl(context):
    assert "MakeMyTrip" in context.driver.title or "makemytrip" in context.driver.current_url, "Application did not launch correctly"
    logger.info("Application launched successfully")

@given('User loads test data from Excel "{file_name}"')
def step_impl(context, file_name):
    filepath = os.path.join("testdata", file_name)
    context.train_data = ExcelReader.get_test_data(filepath, sheet_name="TrainBookingData")
    logger.info(f"Loaded test data for passenger: {context.train_data.get('Passenger_Name')}")

# HOME PAGE & NAVIGATION

@when('User closes the login popup')
def step_impl(context):
    context.home_page.close_popup()

@when('User navigates to the Trains section')
def step_impl(context):
    context.home_page.select_train_tab()

@then('the train search dashboard should be visible')
def step_impl(context):
    current_url = context.driver.current_url.lower()
    assert "railways" in current_url, f"Expected to be on Railways dashboard, but URL is: {current_url}"
    logger.info("Train search dashboard is visible")

@when('User enters source station from Excel')
def step_impl(context):
    source = context.train_data['from_station']
    context.home_page.select_station(HomeLocators.FROM_FIELD, source)

@when('User enters destination station from Excel')
def step_impl(context):
    destination = context.train_data['to_station']
    context.home_page.select_station(HomeLocators.TO_FIELD, destination)

@when('User selects a travel date')
def step_impl(context):
    context.home_page.select_date()

@when('User selects the class type')
def step_impl(context):
    context.home_page.select_class()

@when('User clicks on Search Trains button')
def step_impl(context):
    context.home_page.click_search()

# TRAIN LISTING RESULTS PAGE

@then('the train listing results page should be loaded')
def step_impl(context):
    context.train_page.verify_train_search_result()
    current_url = context.driver.current_url.lower()
    assert "delhi" in current_url or "lucknow" in current_url, "Train listing results page did not load correctly."
    logger.info("Train listing results page successfully validated.")

@when('User applies the AC and Available filters')
def step_impl(context):
    context.train_page.apply_ac_filter()
    context.train_page.apply_available_filter()

@when('User selects the first available train ticket')
def step_impl(context):
    context.train_page.select_first_available_train_ticket()

@then('the specific train details page should be loaded')
def step_impl(context):
    element = context.driver.find_element(*PassengerLocators.TRAIN_DETAILS_LOADED)
    assert element.is_displayed(), "The train details box did not load on the page."
    logger.info("POM LOG: Successfully verified that the train details box is loaded.")

# PASSENGER DETAILS PAGE

@when('User opens the add traveller modal and enters passenger details from Excel')
def step_impl(context):
    context.passenger_page.open_add_traveller_modal()
    name = context.train_data['Passenger_Name']
    age = str(context.train_data['Passenger_Age'])
    gender = context.train_data['Passenger_Gender']
    context.passenger_page.fill_traveller_details_and_submit(name, age, gender)

@when('User enters IRCTC username from Excel')
def step_impl(context):
    irctc_user = context.train_data['IRCTC_ID']
    context.passenger_page.enter_irctc_id(irctc_user)

@when('User fills contact details from Excel')
def step_impl(context):
    email = context.train_data['Email']
    phone = str(context.train_data['Mobile_Number'])
    context.passenger_page.fill_contact_details(email, phone)

@when('User selects cancellation insurance and accepts mandatory terms')
def step_impl(context):
    context.passenger_page.select_cancellation_insurance()
    context.passenger_page.click_mandatory_checkbox()

@when('User proceeds to payment')
def step_impl(context):
    context.passenger_page.click_pay_and_book_now()

# PAYMENT PAGE

@then('the payment page should be loaded and credit card option selected')
def step_impl(context):
    context.payment_page.select_credit_card_option()
    current_url = context.driver.current_url.lower()
    assert "payment" in current_url or "checkout" in current_url, f"Failed to reach the payment page. Current URL: {current_url}"
    logger.info("Payment page validated and credit card option selected.")

@when('User enters credit card details from Excel')
def step_impl(context):
    card_no = str(int(float(context.train_data['CARD_NUMBER'])))
    expiry = context.train_data['EXPIRY']
    cvv = str(int(float(context.train_data['CVV'])))
    name = context.train_data['Passenger_Name']
    context.payment_page.enter_card_details(card_no, expiry, cvv, name)


@then('the payment continue button should become active')
def step_impl(context):
    continue_btn = context.driver.find_element(*PaymentLocators.PAYMENT_CONTINUE_BUTTON)
    assert continue_btn.is_enabled(), "The Continue button is disabled. The card details might have triggered a validation error."

    # Assert that we are still safely on the checkout or payment screen
    assert "payment" in context.driver.current_url.lower() or "checkout" in context.driver.current_url.lower(), "Unexpectedly navigated away from the payment page."

    logger.info("POM LOG: Payment Continue button successfully validated as active. Test safely completed.")