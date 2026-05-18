import pytest
from utils.excel_reader import ExcelReader
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from pages.review_page import ReviewPage
from pages.payment_page import PaymentPage

excel = ExcelReader("data/train_data.xlsx", "train_search_data")
test_data = excel.get_data()

@pytest.mark.parametrize("dataset", test_data)
def test_train_booking_flow(driver, logger, dataset):
    logger.info(f"Starting test with dataset: {dataset}")

    # Step 1: Handle login popup
    login_page = LoginPage(driver, logger)
    login_page.handle_login_popup(dataset["Mobile_Number"])

    # Step 2: Navigate to trains
    home_page = HomePage(driver, logger)
    home_page.open_trains_tab()
    home_page.click_book_train()

    # Step 3: Search train
    train_page = TrainPage(driver, logger)
    train_page.search_train(dataset["From"], dataset["To"], dataset["Travel Date"], dataset["Class"])
    train_page.select_train()

    # Step 4: Passenger details
    passenger_page = PassengerPage(driver, logger)
    passenger_page.enter_irctc_id(dataset["IRCTC_ID"])
    passenger_page.fill_passenger_details(
        dataset["Passenger_Name"],
        str(dataset["Passenger_Age"]),
        dataset["Passenger_Gender"],
        dataset["Berth_Preference"],
        str(dataset["Mobile_Number"]),
        dataset["Email"]
    )
    passenger_page.continue_booking()

    # Step 5: Review booking
    review_page = ReviewPage(driver, logger)
    review_page.proceed_to_payment()

    # Step 6: Payment
    payment_page = PaymentPage(driver, logger)
    payment_page.select_credit_card()
    payment_page.validate_payment_section()

    logger.info("End-to-end train booking flow completed successfully")

