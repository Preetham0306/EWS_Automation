import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.Networking.TCP_IP_Settings import TCP_IP_Settings
from Scripts.TestSuccessMessage import TestSuccessMessage


class Other_Settings():
    def click_other_settings(self,driver):
        time.sleep(1)
        other_settings = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href=\"/application_param.htm\"]"))
        )
        name = other_settings.text
        other_settings.click()
        return name

    def run(self,driver,logger):
        name = Other_Settings().click_other_settings(driver)

        ftp_printing = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='IP_FTP']")))
        if ftp_printing.get_attribute('class') != 'checked':
            ftp_printing.click()

        web_scan = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='eSCLNetwork']")))
        classes = web_scan.get_attribute("class")
        if "checked" not in classes:
            web_scan.click()

        secure_web_scan = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='SecureeSCL']")))
        if secure_web_scan.get_attribute('class') != 'checked':
            secure_web_scan.click()

        wins_port = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='EnableWINSPort']")))
        if wins_port.get_attribute('class') != 'checked':
            wins_port.click()

        wins_registration = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='WINSRegistration']")))
        if wins_registration.get_attribute('class') != 'checked':
            wins_registration.click()

        try:
            ipp_fax_out = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//label[@for='IPPFaxOut']")))
            if ipp_fax_out.get_attribute('class') != 'checked'and ipp_fax_out.text == "IPP FaxOut":
                ipp_fax_out.click()
        except TimeoutException:
            logger("IPP FaxOut not found")
        TCP_IP_Settings().apply(driver)
        return TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)