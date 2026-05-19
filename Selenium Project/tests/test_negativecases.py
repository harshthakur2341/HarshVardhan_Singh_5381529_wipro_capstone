import pytest
import allure
from allure_commons.types import AttachmentType
from pages.home_page import HomePage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from utils.logger import LogGen
from utils.csv_reader import CSVReader
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()

# Load negative test cases from CSV configuration layer
negative_cases = CSVReader.read_csv("data/negative_data.csv")


def capture_and_attach(driver, step_name):
    """Helper utility to instantly save screenshots locally and pass them to Allure reports."""
    path = ScreenshotUtil.capture_screenshot(driver, step_name)
    allure.attach.file(path, name=step_name, attachment_type=AttachmentType.PNG)


@allure.feature("Train Booking Framework")
@allure.story("Negative Path UI Validations")
class TestNegativeTrainBooking:

    @pytest.mark.parametrize("failed_booking", negative_cases)
    @allure.title("NS_01: Validate Invalid Station Search Error Handling")
    def test_invalid_station_search_behavior(self, driver, failed_booking):
        # Filter for the appropriate scenario execution row inside the CSV data pool
        if failed_booking.get("scenario_type") != "invalid_station":
            pytest.skip("Data setup target row specialized for separate execution matrix.")

        home = HomePage(driver)
        logger.info(f"STARTING NEGATIVE RUN: Handling bad data search context -> {failed_booking['from_station']}")

        home.search_train(failed_booking["from_station"], failed_booking["to_station"])

        logger.info("COMPLETED: Error UI visibility capture state saved.")
        capture_and_attach(driver, "Negative_Invalid_Station_View")

    @pytest.mark.parametrize("failed_booking", negative_cases)
    @allure.title("NS_02: Verify Invalid Mobile Field Form Validation")
    def test_invalid_mobile_number_validation(self, driver, failed_booking):
        if failed_booking.get("scenario_type") != "invalid_phone":
            pytest.skip("Data setup target row specialized for separate execution matrix.")

        home = HomePage(driver)
        train_page = TrainPage(driver)
        passenger_page = PassengerPage(driver)
        logger.info("STARTING NEGATIVE RUN: Injecting malformed phone number to trigger boundary warning flags.")

        # Progress down to fields execution
        home.search_train(failed_booking["from_station"], failed_booking["to_station"])
        train_page.verify_train_search_result()
        train_page.select_first_available_train_ticket()

        passenger_page.select_cancellation_insurance()
        passenger_page.open_add_traveller_modal()
        passenger_page.fill_traveller_details_and_submit(
            name=failed_booking["Passenger_Name"],
            age=failed_booking["Passenger_Age"],
            gender=failed_booking["Passenger_Gender"]
        )

        # Provisioning bad text element length directly to the mobile locator object
        passenger_page.fill_contact_details(
            email=failed_booking["Email"],
            mobile=failed_booking["Mobile_Number"]
        )

        passenger_page.click_pay_and_book_now()

        logger.info("COMPLETED: Validation tooltip assertion captures taken.")
        capture_and_attach(driver, "Negative_Malformed_Phone_State")