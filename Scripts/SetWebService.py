import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from Scripts.Networking.TCP_IP_Settings import TCP_IP_Settings
from Scripts.TestSuccessMessage import TestSuccessMessage


class SetWebService:

    def run(self,driver,printer_ip,logger):
        is_success = True
        driver.get(f"http://{printer_ip}/webserviceDebug.htm")
        name = "Web Proxy"
        if "404" in driver.page_source or "Not Found" in driver.page_source:
            driver.get(f"http://{printer_ip}/hp/webservice")
            logger("Debug page not available")
        else:
            enable_debug_console = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[@for=\"ManualCheck\"]")))
            classes = enable_debug_console.get_attribute("class")
            if "checked" not in classes:
                enable_debug_console.click()

            stack_selection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "stackSelection")))
            select = Select(stack_selection)
            select.select_by_visible_text("PRODXN")

            TCP_IP_Settings().apply(driver)
            is_success = TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)

            time.sleep(1)

        web_service = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href=\"/webservices_config.htm\"]")))
        name = web_service.text
        web_service.click()

        web_services_setup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/webservices_config.htm']"))
        )
        web_services_setup.click()
        try:
            enable_web_services_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "Register"))
            )
            enable_web_services_button.click()

            is_success &= TestSuccessMessage().test_success(driver, name, "//*[@class=\"content\"]/h2", logger)

        except TimeoutException:
            logger("Web Service already on")
        return is_success


