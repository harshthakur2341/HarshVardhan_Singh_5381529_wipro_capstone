import allure
import undetected_chromedriver as uc  # upgraded framework import
from utils.logger import LogGen
from utils.screenshot_utils import ScreenshotUtil
from utils.config_reader import ConfigReader

# Import Page Objects
from pages.home_page import HomePage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from pages.payment_page import PaymentPage

logger = LogGen.loggen()


def before_scenario(context, scenario):
    logger.info(f"========== STARTING SCENARIO: {scenario.name} ==========")

    try:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        # FIX: Force version_main to match your local browser version (148)
        context.driver = uc.Chrome(options=options, version_main=148)
        logger.info("STEALTH DRIVER INITIALIZED SUCCESSFULLY WITH CHROME 148 PROFILE")

    except Exception as e:
        logger.error(f"FAILED TO INITIALIZE DRIVER: {str(e)}")
        raise Exception("Stealth driver initialization failed")

    context.driver.implicitly_wait(ConfigReader.get_implicit_wait())

    # Initialize POM
    context.home_page = HomePage(context.driver)
    context.train_page = TrainPage(context.driver)
    context.passenger_page = PassengerPage(context.driver)
    context.payment_page = PaymentPage(context.driver)

    # Launch Application
    base_url = ConfigReader.get_base_url()
    logger.info(f"OPENING WEBSITE: {base_url}")
    context.driver.get(base_url)


def after_step(context, step):
    try:
        safe_step_name = "".join(c for c in str(step.name) if c.isalnum() or c in (' ', '_', '-')).strip()
        short_name = safe_step_name[:25].replace(" ", "_")

        if step.status == "failed":
            logger.error(f"STEP FAILED: {step.name}")
            path = ScreenshotUtil.capture_screenshot(context.driver, f"FAIL_{short_name}")
            with open(path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Failed: {step.name}",
                              attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logger.error(f"SCREENSHOT HOOK FAILED: {str(e)}")


def after_scenario(context, scenario):
    logger.info(f"========== CLOSING SCENARIO: {scenario.name} ==========")
    if hasattr(context, 'driver'):
        context.driver.quit()
        logger.info("BROWSER CLOSED SUCCESSFULLY")


def after_all(context):
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except OSError:
            # Silently ignore the OS handle error as the browser is already closed
            pass