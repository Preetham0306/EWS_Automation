import os
import shutil
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Utilities.user_context import get_user_ip


class TestSuccessMessage:
    def delete(self):
        screenshot_folder = f"Screenshots/{get_user_ip()}"
        if os.path.exists(screenshot_folder):
            shutil.rmtree(screenshot_folder)
        os.makedirs(screenshot_folder)

    def test_success(self,driver,name, xpath,logger):
        screenshot_folder = f"Screenshots/{get_user_ip()}"
        try:
            success_message = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
            if "failed" in success_message or "Error" in success_message or "Welcome" in success_message:
                screenshot_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = os.path.join(screenshot_folder, screenshot_name)
                driver.save_screenshot(screenshot_path)
                logger(name + "  failed : " + name + " Screenshot Saved\n")
                logger(f'SCREENSHOT::{screenshot_folder}/{screenshot_name}')
                return False

        except TimeoutException:
            screenshot_name = f"{name}_TimeOutException_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path = os.path.join(screenshot_folder, screenshot_name)
            logger(f'SCREENSHOT::{screenshot_folder}/{screenshot_name}')
            driver.save_screenshot(screenshot_path)
        return True