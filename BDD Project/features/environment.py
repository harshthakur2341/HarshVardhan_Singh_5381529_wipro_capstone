import time
import os
import allure

from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_utils import ScreenshotUtil
from utils.config_reader import ConfigReader

logger = LogGen.loggen()


# Import all your page object classes at the top of environment.py
from pages.home_page import HomePage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from pages.payment_page import PaymentPage

def before_scenario(context, scenario):
    logger.info(f"========== STARTING SCENARIO: {scenario.name} ==========")

    # Initialize Driver
    context.driver = Driver(uc=True)
    context.driver.maximize_window()
    context.driver.implicitly_wait(ConfigReader.get_implicit_wait())

    # Open URL
    base_url = "https://www.makemytrip.com/railways/"
    context.driver.get(base_url)

    # --- INITIALIZE ALL PAGE OBJECTS ---
    context.home_page = HomePage(context.driver)
    context.train_page = TrainPage(context.driver)
    context.passenger_page = PassengerPage(context.driver)
    context.payment_page = PaymentPage(context.driver)
    # ------------------------------------

    time.sleep(2)
    logger.info(f"CURRENT URL: {context.driver.current_url}")

def after_step(context, step):

    try:

        if step.status == "failed":

            logger.error(
                f"STEP FAILED: {step.name} - CAPTURING SCREENSHOT"
            )

            path = ScreenshotUtil.capture_screenshot(
                context.driver,
                f"FAIL_{step.name[:20]}"
            )

            allure.attach.file(
                path,
                name=step.name,
                attachment_type=allure.attachment_type.PNG
            )

        elif step.status == "passed":

            logger.info(
                f"STEP PASSED: {step.name} - CAPTURING SCREENSHOT"
            )

            path = ScreenshotUtil.capture_screenshot(
                context.driver,
                f"PASS_{step.name[:20]}"
            )

            allure.attach.file(
                path,
                name=step.name,
                attachment_type=allure.attachment_type.PNG
            )

    except Exception as e:

        logger.error(
            f"SCREENSHOT FAILED: {str(e)}"
        )


def after_scenario(context, scenario):

    logger.info(
        f"========== CLOSING SCENARIO: {scenario.name} =========="
    )

    if hasattr(context, 'driver'):

        try:

            with open("logs/automation.log", "r") as log_file:

                allure.attach(
                    log_file.read(),
                    name="Execution Logs",
                    attachment_type=allure.attachment_type.TEXT
                )

            context.driver.quit()

            logger.info(
                "BROWSER CLOSED SUCCESSFULLY"
            )

        except Exception as e:

            logger.error(
                f"ERROR CLOSING BROWSER: {str(e)}"
            )


def after_all(context):

    print(
        "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
    )

    os.system(
        "allure generate reports/allure-results -o reports/allure-report --clean"
    )

    os.system(
        "allure open reports/allure-report"
    )