import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_factory import DriverFactory


class SetFax:
    def run(self,driver,fax_number, logger):
        time.sleep(1)
        fax = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/hp/device/Fax/Index']"))
        )
        name = fax.text
        fax.click()
        fax_enabled = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"FaxEnabledCheckBox\"]")))
        if fax_enabled.get_attribute('class') != 'checked':
            fax_enabled.click()

        select_fax_method = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "FaxMethodDropdown"))))
        select_fax_method.select_by_visible_text("Internal Modem")

        internal_modem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TabbedController__FaxTabsController__AnalogFaxController")))
        internal_modem.click()

        set_location = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DeviceModemSettingsCountryRegion"))))
        set_location.select_by_visible_text("India")

        set_company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DeviceModemSettingsCompanyName")))
        set_company_name.clear()
        set_company_name.send_keys("Mphasis")

        set_fax_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DeviceModemSettingsPhoneNumber")))
        set_fax_number.clear()
        set_fax_number.send_keys(fax_number)

        DriverFactory.click_apply(driver)
        return TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)
