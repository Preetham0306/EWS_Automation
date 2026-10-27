import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Scripts.TestSuccessMessage import TestSuccessMessage


class SignUp:
    def run(self,driver,password, logger):
        signup_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "EwsLogin")))
        signup_button.click()

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "PasswordTextBox")))
        password_field.send_keys(password)

        sign_in = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signInOk")))
        sign_in.click()
        time.sleep(1)
        return TestSuccessMessage().test_success(driver,'SignUp',"//div[@class=\"user-content\"]/p", logger)