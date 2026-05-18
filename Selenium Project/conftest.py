import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.logger import Logger



@pytest.fixture(scope="session")
def logger():
    return Logger("MakeMyTripAutomation").get_logger()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="edge", help="Browser option: edge or chrome")

@pytest.fixture(scope="function")
def driver(request, logger):
    browser = request.config.getoption("--browser").lower()
    logger.info(f"Launching browser: {browser}")

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    else:  # default edge
        options = EdgeOptions()
        options.add_argument("--inprivate")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)

    driver.maximize_window()
    driver.get("https://www.makemytrip.com/railways")
    driver.delete_all_cookies()
    driver.refresh()
    logger.info("Browser launched, cookies cleared, page refreshed")

    yield driver

    logger.info("Closing browser session")
    driver.quit()

# Screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            item._report_sections.append(("call", "screenshot", screenshot_path))




'''import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager

from utils.config_reader import ConfigReader
from utils.logger import LogGen
logger = LogGen.loggen()


@pytest.fixture(scope="function")
def driver():
    logger.info("==================================================")
    logger.info(f'Starting test!!')
    logger.info(f'Reading ')
    browser = ConfigReader.get("browser").strip() .lower()
    print(f"Browser from config: '{browser}'")

    base_url = ConfigReader.get("base_url").strip() .lower()
    # headless = ConfigReader.get("headless").strip()

    if browser == "edge":
            edge_options = EdgeOptions()
            edge_options.add_argument("--start-maximized")
            edge_options.add_argument("--disable-notifications")
            edge_options.add_argument("--disable-infobars")
            edge_options.add_argument("--disable-extensions")
            # if headless:
            #     edge_options.add_argument("--headless")
            driver = webdriver.Edge(options=edge_options)
    elif browser == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            # if headless:
            #     chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )
    else:
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        # if headless:
        #     edge_options.add_argument("--headless")
        driver = webdriver.Edge(options=edge_options)

    logger.info(f'Opened browser: {browser}')
    driver.get(base_url)
    logger.info(f'Url loaded: {base_url}')
    yield driver
    driver.quit()

    logger.info(f'Closing browser: {browser}')
    logger.info(f'ENDING TEST')
    logger.info('================================================')



import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.config_reader import ConfigReader
from utils.logger import LogGen

logger = LogGen.loggen()


@pytest.fixture(scope="function")
def driver():

    logger.info("==================================================")
    logger.info("Starting test!!")

    browser = ConfigReader.get("browser").strip().lower()
    base_url = ConfigReader.get("base_url").strip()

    print(f"Browser from config: '{browser}'")

    if browser == "edge":

        edge_options = EdgeOptions()

        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")

        edge_options.add_argument("--inprivate")
        

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=edge_options
        )

    elif browser == "chrome":

        chrome_options = ChromeOptions()

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

    else:

        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--inprivate")

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=edge_options
        )

    logger.info(f"Opened browser: {browser}")

    driver.get(base_url)

    driver.delete_all_cookies()

    driver.refresh()

    logger.info(f"URL loaded: {base_url}")

    yield driver

    driver.quit()

    logger.info(f"Closing browser: {browser}")
    logger.info("ENDING TEST")
    logger.info("==================================================")'''