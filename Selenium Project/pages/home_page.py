import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import LogGen

logger = LogGen.loggen()


class HomePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

    def close_popup(self):

        try:

            time.sleep(2)

            close_btn = self.driver.find_element(
                By.XPATH,
                "//span[@data-cy='closeModal']"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close_btn
            )

            logger.info(
                "LOGIN POPUP CLOSED"
            )

            time.sleep(1)

        except:

            try:

                body = self.driver.find_element(
                    By.TAG_NAME,
                    "body"
                )

                body.click()

                logger.info(
                    "CLICKED OUTSIDE POPUP"
                )

                time.sleep(1)

            except:

                logger.info(
                    "NO POPUP FOUND"
                )

    def select_train_tab(self):

        try:

            train_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(),'Trains')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                train_tab
            )

            logger.info(
                "TRAIN TAB CLICKED"
            )

            time.sleep(2)

        except Exception as e:

            logger.info(
                f"TRAIN TAB ISSUE: {str(e)}"
            )

    def select_station(self, field_xpath, station):

        station_field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    field_xpath
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            station_field
        )

        logger.info(
            f"CLICKED FIELD: {station}"
        )

        time.sleep(2)

        active_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'From') or contains(@placeholder,'To')]"
                )
            )
        )

        active_input.send_keys(
            Keys.CONTROL + "a"
        )

        active_input.send_keys(
            Keys.DELETE
        )

        time.sleep(1)

        active_input.send_keys(station)

        logger.info(
            f"TYPED STATION: {station}"
        )

        time.sleep(3)

        first_option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "(//ul[contains(@class,'react-autosuggest')]//li)[1]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            first_option
        )

        logger.info(
            f"SELECTED STATION: {station}"
        )

        time.sleep(2)

    def select_date(self):

        try:

            date_box = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//label[@for='travelDate']"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                date_box
            )

            logger.info(
                "DATE BOX CLICKED"
            )

            time.sleep(2)

            target_date = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@aria-label='Sat May 30 2026']"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                target_date
            )

            logger.info(
                "30 MAY 2026 DATE SELECTED"
            )

            time.sleep(2)

        except Exception as e:

            logger.info(
                f"DATE ISSUE: {str(e)}"
            )

            raise

    def select_class(self):

        try:

            class_box = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(),'Class')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                class_box
            )

            logger.info(
                "CLASS DROPDOWN CLICKED"
            )

            time.sleep(2)

            sleeper_class = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//li[contains(text(),'Sleeper')]"
                    )
                )
            )

            sleeper_class.click()

            logger.info(
                "SLEEPER CLASS SELECTED"
            )

            time.sleep(2)

        except Exception as e:

            logger.info(
                f"CLASS ISSUE: {str(e)}"
            )

    def click_search(self):

        logger.info(
            "CLICKING SEARCH BUTTON"
        )

        search_btn = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[contains(text(),'Search')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_btn
        )

        time.sleep(2)

        search_btn.click()

        logger.info(
            "SEARCH BUTTON CLICKED"
        )

        time.sleep(5)

    def search_train(self, from_station, to_station):

        logger.info(
            "STARTING TRAIN SEARCH"
        )

        self.close_popup()

        time.sleep(2)

        from_field = "//label[@for='fromCity']"

        to_field = "//label[@for='toCity']"

        logger.info(
            f"FROM STATION: {from_station}"
        )

        self.select_station(
            from_field,
            from_station
        )

        logger.info(
            f"TO STATION: {to_station}"
        )

        self.select_station(
            to_field,
            to_station
        )

        self.select_date()

        self.click_search()

        logger.info(
            "TRAIN SEARCH COMPLETED"
        )