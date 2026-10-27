from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DriverFactory:

    @staticmethod
    def get_driver():
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.page_load_strategy = "eager"
        driver = webdriver.Edge(options=options)
        driver.maximize_window()
        return driver

    @staticmethod
    def click_apply(driver):
        apply = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "FormButtonSubmit")))
        apply.click()