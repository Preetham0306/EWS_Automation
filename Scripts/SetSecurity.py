import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_factory import DriverFactory


class SetSecurity():

    def open_security_page(self, driver):
        time.sleep(1)
        security = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "SecurityPages")))
        name = security.text
        security.click()
        return name

    def set_new_password(self, driver,password):
        new_password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "newPassword")))
        new_password_field.send_keys(password)

        verify_password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "verifyPassword")))
        verify_password_field.send_keys(password)

    def run(self, driver, password, logger):
        name = SetSecurity().open_security_page(driver)

        try:
            old_password_field = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class=\"control data\"]/input")))

            if not bool(old_password_field.get_attribute('value')):
                raise Exception(
                    f"Password is not set."
                )
        except TimeoutException as e:
            old_password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "oldPassword")))
            old_password_field.send_keys(password)

        SetSecurity().set_new_password(driver,password)

        access_code = "12345678"
        set_access_code = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ServicePin")))
        set_access_code.clear()
        set_access_code.send_keys(access_code)

        verify_access_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VerifyServicePin")))
        verify_access_code.clear()
        verify_access_code.send_keys(access_code)


        cross_site_checkbox =  WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"csrfPrevention\"]")))
        if cross_site_checkbox.get_attribute('class') == 'checked':
            cross_site_checkbox.click()

        enable_remote_user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[@for=\"enableRemoteUserAutoCapture\"]")))
        if enable_remote_user.get_attribute('class') != 'checked':
            enable_remote_user.click()
        #
        enable_device_access = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"EnableDeviceAccess\"]")))
        if enable_device_access.get_attribute('class') != 'checked':
            enable_device_access.click()

        ps_operators = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"EnableDisablePostScriptPassword\"]")))
        if ps_operators.get_attribute('class') != 'checked':
            ps_operators.click()

        allow_firmware_upgrades = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"IsPrintPathEnabled\"]")))
        if allow_firmware_upgrades.get_attribute('class') != 'checked':
            allow_firmware_upgrades.click()

        pjl_drive_access = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"PJLFileSystemAccess\"]")))
        if pjl_drive_access.get_attribute('class') != 'checked':
            pjl_drive_access.click()

        ps_drive_access = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"PostScriptFileSystemAccess\"]")))
        if ps_drive_access.get_attribute('class') != 'checked':
            ps_drive_access.click()

        device_usb = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for=\"disableDirectConnect\"]")))
        if device_usb.get_attribute('class') != 'checked':
            device_usb.click()

        DriverFactory.click_apply(driver)
        return TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)
