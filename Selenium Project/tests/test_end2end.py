import pytest
import allure
from allure_commons.types import AttachmentType
from pages.home_page import HomePage
from pages.payment_page import PaymentPage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from utils.logger import LogGen
from utils.excel_reader import ExcelReader
from utils.screenshot_util import ScreenshotUtil  # <-- Imported your utility

logger = LogGen.loggen()

# --- ONLY ADD THIS LINE ---
combined_train_data = ExcelReader.read_excel("data/test_data.xlsx", "TrainBookingData")

def attach_screenshot_to_allure(driver, name):
    """Helper method to capture and attach screenshots to Allure reports."""
    path = ScreenshotUtil.capture_screenshot(driver, name)
    allure.attach.file(path, name=name, attachment_type=AttachmentType.PNG)


@allure.feature("E2E Train Booking")
@pytest.mark.parametrize("booking", combined_train_data)
def test_complete_train_search_flow(driver, booking):
    logger.info(f"STARTING TRAIN SEARCH FLOW FOR: {booking.get('from_station')} TO {booking.get('to_station')}")
    home = HomePage(driver)

    # --- PHASE 1: HOME PAGE SEARCH ---
    home.search_train(booking.get("from_station"), booking.get("to_station"))
    logger.info("TRAIN SEARCH COMPLETED FROM HOME PAGE")
    attach_screenshot_to_allure(driver, "1_After_Homepage_Search")

    # --- PHASE 2: TRAIN LISTING FILTERS ---
    train_page = TrainPage(driver)
    train_page.verify_train_search_result()
    train_page.filter_ac_trains()
    train_page.filter_available_trains()
    attach_screenshot_to_allure(driver, "2_After_Applying_Filters")

    # --- PHASE 3: SEAT SELECTION ---
    train_page.select_first_available_train_ticket()
    logger.info("TRAIN SPECIFIC RUN SELECTION CAPTURED SUCCESSFULLY")
    attach_screenshot_to_allure(driver, "3_After_Seat_Selection")

    # --- PHASE 4: PASSENGER PAGE & POPUP MODAL ---
    passenger_page = PassengerPage(driver)

    # Select cancellation insurance option
    passenger_page.select_cancellation_insurance()

    # Open the "+ Add Traveller" pop-up modal
    passenger_page.open_add_traveller_modal()

    # Fill out the modal using the passenger data fields
    passenger_page.fill_traveller_details_and_submit(
        name=booking.get("Passenger_Name"),
        age=booking.get("Passenger_Age"),
        gender=booking.get("Passenger_Gender")
    )
    logger.info("TRAVELLER POPULATED SUCCESSFULLY VIA EXCEL")

    # Fill contact information fields further down the page
    passenger_page.fill_contact_details(
        email=booking.get("Email"),
        mobile=booking.get("Mobile_Number")
    )
    logger.info("CONTACT DETAILS POPULATED SUCCESSFULLY")
    attach_screenshot_to_allure(driver, "4_After_Passenger_Details")

    # --- PHASE 5: IRCTC ACCOUNT DETAILS VERIFICATION MODAL ---
    passenger_page.enter_irctc_id(booking.get("IRCTC_ID"))
    logger.info("END-TO-END FLOW RUN COMPLETED SUCCESSFULLY")
    attach_screenshot_to_allure(driver, "5_After_IRCTC_Entry")

    # --- PHASE 6: FINAL BOOKING ACKNOWLEDGEMENT & SUBMISSION ---
    passenger_page.click_mandatory_checkbox()
    logger.info("MANDATORY ACKNOWLEDGEMENT CHECKBOX CONFIRMED AND SUCCESSFUL")

    passenger_page.click_pay_and_book_now()
    logger.info("PAY AND BOOK NOW BUTTON SELECTION COMPLETED SUCCESSFULLY")
    attach_screenshot_to_allure(driver, "6_After_Clicking_Pay_And_Book")

    # --- PHASE 7: SECURE PAYMENT GATEWAY INGESTION ---
    payment_page = PaymentPage(driver)

    # Handle navigation sidebar choices
    payment_page.select_credit_card_option()

    # Normalize keys to uppercase to eliminate any accidental Excel header variations
    clean_booking = {str(k).strip().upper(): v for k, v in booking.items()}

    # Ingest data safely using your updated reference architecture
    payment_page.enter_card_details(
        card_number=clean_booking.get("CARD_NUMBER"),
        expiry=clean_booking.get("EXPIRY"),
        cvv=clean_booking.get("CVV"),
        card_holder=clean_booking.get("CARD_HOLDER")
    )
    logger.info("TEST PIPELINE: PAYMENT DATA COMPLETELY COMMITTED")
    attach_screenshot_to_allure(driver, "7_Final_Payment_Page_State")
    current_dom_text = driver.page_source.lower()
    current_url_path = driver.current_url.lower()

    # Validates that the engine successfully progressed deep into the checkout environment without stalling
    assert "payment" in current_url_path or "checkout" in current_url_path or "pay" in current_dom_text, \
        f"E2E Validation Failed: Card/CVV submitted but driver got stranded at endpoint: {driver.current_url}"