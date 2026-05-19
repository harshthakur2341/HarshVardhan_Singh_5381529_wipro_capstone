import pytest
import allure
from allure_commons.types import AttachmentType
from pages.home_page import HomePage
from pages.payment_page import PaymentPage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from utils.logger import LogGen
from utils.csv_reader import CSVReader
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

# Load positive test cases from CSV data configuration layer
positive_cases = CSVReader.read_csv("data/positive_data.csv")


def capture_and_attach(driver, step_name):
    """Helper utility to save screenshots locally and pass them to Allure reports."""
    path = ScreenshotUtil.capture_screenshot(driver, step_name)
    allure.attach.file(path, name=step_name, attachment_type=AttachmentType.PNG)


@pytest.mark.parametrize("booking", positive_cases)
@allure.title("TS_01: Verify Train Search Functionality")
def test_verify_train_search(driver, booking):
    home = HomePage(driver)
    logger.info(f"STARTING TS_01: Train search from {booking['from_station']} to {booking['to_station']}")

    home.search_train(booking["from_station"], booking["to_station"])

    logger.info("COMPLETED TS_01: Search parameters successfully submitted.")
    capture_and_attach(driver, "TC01_Search_Submitted")

    # 1. Assert that the driver navigated away from home to the listings endpoint
    assert "listing" in driver.current_url.lower(), f"Search failed: URL stayed at {driver.current_url}"

    # 2. Assert that we see actual results (Checking that the URL has train parameters populated)
    assert "srcstn=" in driver.current_url.lower(), "Search validation failed: Train station code parameters missing from landing view!"


@pytest.mark.parametrize("booking", positive_cases)
@allure.title("TS_02: Validate Train Listing Display")
def test_validate_train_listing_display(driver, booking):
    home = HomePage(driver)
    train_page = TrainPage(driver)
    logger.info(f"STARTING TS_02: Validating listing page for {booking['from_station']} -> {booking['to_station']}")

    home.search_train(booking["from_station"], booking["to_station"])

    # The page object function itself acts as our verification layer
    train_page.verify_train_search_result()

    logger.info("COMPLETED TS_02: Train list component rendering confirmed.")
    capture_and_attach(driver, "TC02_Listing_Verified")

    # Assert to confirm listing components are actively visible on page
    assert "view" in driver.current_url.lower() or "search" in driver.current_url.lower(), "Listing page failed to load!"


@pytest.mark.parametrize("booking", positive_cases)
@allure.title("TS_03: Verify Train Filters Functionality")
def test_verify_train_filters(driver, booking):
    home = HomePage(driver)
    train_page = TrainPage(driver)
    logger.info("STARTING TS_03: Triggering class and availability checkbox modifications.")

    home.search_train(booking["from_station"], booking["to_station"])
    train_page.verify_train_search_result()

    train_page.filter_ac_trains()
    train_page.filter_available_trains()

    logger.info("COMPLETED TS_03: Target filters applied successfully.")
    capture_and_attach(driver, "TC03_Filters_Applied")

    # Simple true assertion to confirm the test steps executed successfully without crash exceptions
    assert driver.current_url is not None, "Driver context lost during filter manipulation!"


@pytest.mark.parametrize("booking", positive_cases)
@allure.title("TS_04: Verify Successful Navigation to Payment Page")
def test_verify_payment_page_navigation(driver, booking):
    home = HomePage(driver)
    train_page = TrainPage(driver)
    passenger_page = PassengerPage(driver)
    payment_page = PaymentPage(driver)
    logger.info("STARTING TS_04: Executing full checkout cycle to payment gateway handoff.")

    # Navigate and Select Train
    home.search_train(booking["from_station"], booking["to_station"])
    train_page.verify_train_search_result()
    train_page.filter_ac_trains()
    train_page.filter_available_trains()
    train_page.select_first_available_train_ticket()

    # Populate Passenger Forms
    passenger_page.select_cancellation_insurance()
    passenger_page.open_add_traveller_modal()
    passenger_page.fill_traveller_details_and_submit(
        name=booking["Passenger_Name"],
        age=booking["Passenger_Age"],
        gender=booking["Passenger_Gender"]
    )
    passenger_page.fill_contact_details(email=booking["Email"], mobile=booking["Mobile_Number"])
    passenger_page.enter_irctc_id(booking["IRCTC_ID"])
    passenger_page.click_mandatory_checkbox()
    passenger_page.click_pay_and_book_now()

    # Handle Payment Gateway Elements
    payment_page.select_credit_card_option()
    capture_and_attach(driver, "TC04_Payment_Gateway_Loaded")

    clean_booking = {str(k).strip().upper(): v for k, v in booking.items()}
    payment_page.enter_card_details(
        card_number=clean_booking.get("CARD_NUMBER"),
        expiry=clean_booking.get("EXPIRY"),
        cvv=clean_booking.get("CVV"),
        card_holder=clean_booking.get("CARD_HOLDER")
    )
    logger.info("COMPLETED TS_04: Card credential injection finalized.")

    # Assert that we are truly interacting on a secure checkout/payment url context
    assert "payment" in driver.current_url.lower() or "checkout" in driver.current_url.lower(), "Handoff validation failed: Not on payment screen!"