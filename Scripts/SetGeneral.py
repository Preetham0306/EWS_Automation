import time
from datetime import datetime
import re

from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_factory import DriverFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SetGeneral:
    def run(self, driver, ip1, logger):
        xpath = "//div[@class=\"content\"]/h2"
        general = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "SettingsPages")))
        name = general.text
        general.click()

        dateAndTime = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DateAndTime")))
        dateAndTime.click()

        timeZoneSettings = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TimeZoneSettings")))
        timeZoneSettings.click()

        time.sleep(1)

        currentTimeZone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CurrentTimeZone")))
        select = Select(currentTimeZone)
        select.select_by_visible_text("(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi")

        DriverFactory.click_apply(driver)
        is_success = TestSuccessMessage().test_success(driver, name, xpath, logger)

        nts_settings_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "NTSSettings")))
        nts_settings_button.click()

        network_time_server_address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ServerAddress")))
        network_time_server_address.clear()
        network_time_server_address.send_keys(ip1)

        time_difference = 2
        while time_difference > 1:
            synchronize_now_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "SyncNow")))
            synchronize_now_button.click()
            current_time = int(datetime.now().strftime("%H%M"))
            time.sleep(2)
            time_server_status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"NetworkTimeServerSettingsViewSectionId\"]/div[2]/div/div/div[3]/div/em"))).text
            match = re.search(r'at (\d{2}:\d{2}):\d{2}', time_server_status)
            synchronized_time = 0
            if match:
                synchronized_time = int(match.group(1).replace(":", ""))
            time_difference = abs(synchronized_time - current_time)

        DriverFactory.click_apply(driver)
        is_success &= TestSuccessMessage().test_success(driver, name, xpath, logger)
        return is_success


