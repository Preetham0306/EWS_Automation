import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.Networking.TCP_IP_Settings import TCP_IP_Settings
from Scripts.TestSuccessMessage import TestSuccessMessage


class Network_Settings:
    def run(self,driver, logger):
        time.sleep(1)
        network_settings = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href=\"/snmp_creds.html\"]"))
        )
        name = network_settings.text
        network_settings.click()

        set_community_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "setcomm")))
        set_community_name.clear()
        set_community_name.send_keys("public")

        confirm_set_community_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "confsetcomm")))
        confirm_set_community_name.clear()
        confirm_set_community_name.send_keys("public")

        get_community_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "getcomm")))
        get_community_name.clear()
        get_community_name.send_keys("public")

        confirm_get_community_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "confgetcomm")))
        confirm_get_community_name.clear()
        confirm_get_community_name.send_keys("public")

        radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for=\"snmpv1RW\"]"))
        )
        radio.click()

        TCP_IP_Settings().apply(driver)
        return TestSuccessMessage().test_success(driver,name, "//div[@class=\"content\"]/h2", logger)
        #time.sleep(3)