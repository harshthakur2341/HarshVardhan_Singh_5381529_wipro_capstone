

import pytest
from selenium import webdriver

from selenium.webdriver.chrome.service import (
    Service as ChromeService
)

from selenium.webdriver.edge.options import (
    Options as EdgeOptions
)

from selenium.webdriver.chrome.options import (
    Options as ChromeOptions
)

from webdriver_manager.chrome import (
    ChromeDriverManager
)

from utils.config_reader import ConfigReader
from utils.logger import LogGen


logger = LogGen.loggen()


@pytest.fixture(scope="module")
def driver():

    # Read configuration
    browser = ConfigReader.get(
        "browser"
    ).strip().lower()

    base_url = ConfigReader.get(
        "base_url"
    ).strip()

    implicit_wait = int(
        ConfigReader.get(
            "implicit_wait"
        )
    )

    timeout = int(
        ConfigReader.get(
            "timeout"
        )
    )

    # IMPORTANT FIX
    headless = ConfigReader.get(
        "headless"
    ).strip().lower() == "true"

    logger.info(
        "======================================="
    )

    logger.info("Starting Test")

    logger.info(
        f"Browser : {browser}"
    )

    logger.info(
        f"Base URL : {base_url}"
    )

    logger.info(
        f"Implicit Wait : {implicit_wait}"
    )

    logger.info(
        f"Timeout : {timeout}"
    )

    logger.info(
        f"Headless : {headless}"
    )

    # CHROME
    if browser == "chrome":

        chrome_options = ChromeOptions()

        # Browser visible on screen
        chrome_options.add_argument(
            "--start-maximized"
        )

        chrome_options.add_argument(
            "--disable-notifications"
        )

        chrome_options.add_argument(
            "--disable-infobars"
        )

        chrome_options.add_argument(
            "--disable-extensions"
        )

        # Only run headless if true
        if headless:

            chrome_options.add_argument(
                "--headless=new"
            )

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

    # EDGE
    elif browser == "edge":

        edge_options = EdgeOptions()

        edge_options.add_argument(
            "--start-maximized"
        )

        edge_options.add_argument(
            "--disable-notifications"
        )

        edge_options.add_argument(
            "--disable-infobars"
        )

        edge_options.add_argument(
            "--disable-extensions"
        )

        if headless:

            edge_options.add_argument(
                "--headless"
            )

        driver = webdriver.Edge(
            options=edge_options
        )

    # DEFAULT CHROME
    else:

        chrome_options = ChromeOptions()

        chrome_options.add_argument(
            "--start-maximized"
        )

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

    # Waits
    driver.implicitly_wait(
        implicit_wait
    )

    driver.maximize_window()

    logger.info(
        f"Opening URL : {base_url}"
    )

    driver.get(base_url)

    yield driver

    logger.info(
        "Closing Browser"
    )

    driver.quit()

    logger.info(
        "Ending Test"
    )

    logger.info(
        "======================================="
    )


# ALLURE
def pytest_unconfigure(config):
    import os
    import subprocess

    print("\n===== TESTS COMPLETED - GENERATING & OPENING ALLURE REPORT =====")

    results_dir = "reports/allure-results"
    output_report_dir = "reports/allure-report"
    allure_executable = r"C:\allure\bin\allure.bat"

    if os.path.exists(results_dir):
        if os.path.exists(allure_executable):
            print(f"1. Compiling raw data into {output_report_dir}...")

            # Step 1: Generate the permanent HTML files for Git
            generate_command = f'"{allure_executable}" generate "{results_dir}" -o "{output_report_dir}" --clean'
            subprocess.run(generate_command, shell=True)
            print("Permanent Allure report generated successfully!")

            # Step 2: Automatically launch the local server and open the browser
            print("2. Launching report in your default browser...")
            open_command = f'"{allure_executable}" open "{output_report_dir}"'

            # Using Popen keeps the server open in the background so the browser can read it
            subprocess.Popen(open_command, shell=True)

        else:
            print(f"Error: Allure executable not found at {allure_executable}.")
    else:
        print(f"Error: The directory '{results_dir}' was not found.")