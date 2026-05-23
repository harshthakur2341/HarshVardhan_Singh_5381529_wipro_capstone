import os
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.csv_reader import CSVReader
from utils.logger import LogGen
from locators.home_locators import HomeLocators
from locators.passenger_locators import PassengerLocators
from locators.train_locators import TrainLocators

logger = LogGen.loggen()


@given('User extracts test data from CSV "{file_name}" for row "{row_id}"')
def step_impl(context, file_name, row_id):
    filepath = os.path.join("testdata", file_name)
    data_list = CSVReader.read_csv_data(filepath)
    index = int(row_id) - 1

    assert 0 <= index < len(data_list), f"Row ID {row_id} is out of bounds for {file_name}"
    context.train_data = data_list[index]
    logger.info(f"Loaded test data from {file_name}")


@when('User provides search source station from CSV')
def step_impl(context):
    context.home_page.select_station(HomeLocators.FROM_FIELD, context.train_data['from_station'])


@when('User provides invalid search source station from CSV')
def step_impl(context):
    context.home_page.select_station(HomeLocators.FROM_FIELD, context.train_data['from_station'])


@when('User provides search destination station from CSV')
def step_impl(context):
    context.home_page.select_station(HomeLocators.TO_FIELD, context.train_data['to_station'])



@when('User opens the add traveller modal and enters passenger details from CSV')
def step_impl(context):
    context.passenger_page.open_add_traveller_modal()
    context.passenger_page.fill_traveller_details_and_submit(
        context.train_data['Passenger_Name'],
        str(context.train_data['Passenger_Age']),
        context.train_data['Passenger_Gender']
    )


@when('User enters IRCTC username from CSV')
def step_impl(context):
    context.passenger_page.enter_irctc_id(context.train_data['IRCTC_ID'])


@when('User fills contact details from CSV')
def step_impl(context):
    context.passenger_page.fill_contact_details(context.train_data['Email'], str(context.train_data['Mobile_Number']))


@when('User fills contact details with an invalid mobile number from CSV')
def step_impl(context):
    context.passenger_page.fill_contact_details(context.train_data['Email'],
                                                str(context.train_data['Mobile_Number']))


@then('User should see the train search results successfully')
def step_impl(context):
    assert "listing" in context.driver.current_url.lower()
    results_container = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located(TrainLocators.TRAIN_LIST_CONTAINER))
    assert results_container.is_displayed()


@then('User should see available trains listed on the results page')
def step_impl(context):
    assert len(context.driver.find_elements(*TrainLocators.TRAIN_CARD)) > 0


@then('Verify that the train results update successfully based on filters')
def step_impl(context):
    assert len(context.driver.find_elements(*TrainLocators.ACTIVE_FILTER_TAG)) > 0


@then('User should successfully navigate to the payment page')
def step_impl(context):
    # Wait up to 15 seconds for the URL to change to the payment/checkout page
    try:
        WebDriverWait(context.driver, 15).until(
            lambda driver: "payment" in driver.current_url.lower() or "checkout" in driver.current_url.lower()
        )
    except Exception:
        pass

    current_url = context.driver.current_url.lower()

    # Asserting against multiple keywords since MakeMyTrip sometimes uses 'checkout' instead of 'payment'
    assert "payment" in current_url or "checkout" in current_url, \
        f"Failed to reach payment page. Current URL is: {current_url}"

@then('User should see an error message stating stations cannot be the same')
def step_verify_same_station_error(context):
    error_text = context.home_page.get_same_station_error_text()
    assert error_text is not None, "Expected 'Same Station' error message did not appear on the screen."
    expected_phrase = "cannot be the same"
    assert expected_phrase in error_text, f"Expected error to contain '{expected_phrase}', but got: '{error_text}'"

@then('User should see a validation error for the invalid mobile number')
def step_impl(context):
    err = WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located(PassengerLocators.MOBILE_VALIDATION_ERROR))
    assert err.is_displayed()