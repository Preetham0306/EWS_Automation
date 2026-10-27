from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.SetSecurity import SetSecurity
from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_factory import DriverFactory


class Change_Password:
    def run(self, driver,old_password,new_password, logger):
        SetSecurity().open_security_page(driver)

        old_password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "oldPassword")))
        old_password_field.send_keys(old_password)

        SetSecurity().set_new_password(driver,new_password)

        DriverFactory.click_apply(driver)
        return TestSuccessMessage().test_success(driver,"Change_Password",xpath="//div[@class=\"content\"]/h2", logger=logger)
