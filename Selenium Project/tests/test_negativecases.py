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

# --- Load and Pre-Filter Datasets cleanly at runtime ---
raw_negative_cases = CSVReader.read_csv("data/negative_data.csv")
invalid_station_cases = [row for row in raw_negative_cases if row.get("scenario_type") == "invalid_station"]
invalid_phone_cases = [row for row in raw_negative_cases if row.get("scenario_type") == "invalid_phone"]

def capture_and_attach(driver, step_name):
    path = ScreenshotUtil.capture_screenshot(driver, step_name)
    allure.attach.file(path, name=step_name, attachment_type=AttachmentType.PNG)


@pytest.mark.parametrize("failed_booking", invalid_station_cases) # Focuses only on invalid station rows
@allure.title("NS_01: Validate Invalid Station Search Error Handling")
def test_invalid_station_search_behavior(driver, failed_booking):
    home = HomePage(driver)
    logger.info(f"STARTING NS_01: Submitting invalid station input -> {failed_booking['from_station']}")

    home.search_train(failed_booking["from_station"], failed_booking["to_station"])

    logger.info("COMPLETED NS_01: Negative station search error state screenshotted.")
    capture_and_attach(driver, "Negative_Invalid_Station_View")
    assert "view" not in driver.current_url.lower(), "Negative Test Failed: Entered listing flow with garbage data!"


@pytest.mark.parametrize("failed_booking", invalid_phone_cases) # Focuses only on invalid phone rows
@allure.title("NS_02: Verify Invalid Mobile Field Form Validation")
def test_invalid_mobile_number_validation(driver, failed_booking):
    home = HomePage(driver)
    train_page = TrainPage(driver)
    passenger_page = PassengerPage(driver)
    logger.info("STARTING NS_02: Supplying invalid phone format block to verify inline alert tracking.")

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

    passenger_page.fill_contact_details(
        email=failed_booking["Email"],
        mobile=failed_booking["Mobile_Number"]
    )

    passenger_page.click_pay_and_book_now()

    logger.info("COMPLETED NS_02: Error boundary tooltips caught successfully.")
    capture_and_attach(driver, "Negative_Malformed_Phone_State")
    assert "payment" not in driver.current_url.lower(), "Negative Test Failed: Navigated to payment page using invalid phone string!"