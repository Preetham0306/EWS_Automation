import os
from datetime import datetime

from selenium.common.exceptions import TimeoutException

from Utilities.driver_factory import DriverFactory
from Utilities.user_context import get_user_ip


class OpenEWS:

    def run(self, printer_ip,logger,max_retries = 3):
        for attempt in range(max_retries):
            driver = DriverFactory.get_driver()
            try:

                driver.set_page_load_timeout(10)

                driver.get(f"http://{printer_ip}")

                logger("Page Title : " + driver.title)
                logger("Current URL s: " + driver.current_url + "\n")

                return driver

            except TimeoutException:
                logger(f"Attempt {attempt + 1} : Page load timed out\n")
                driver.quit()

        raise Exception(
            f"Unable to open EWS after {max_retries} attempts"
        )