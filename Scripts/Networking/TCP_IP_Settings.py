import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Scripts.TestSuccessMessage import TestSuccessMessage


class TCP_IP_Settings():
    def apply(self,driver):
        time.sleep(1)
        apply = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Apply")))
        apply.click()

    def click_networking(self,driver):
        time.sleep(1)
        networking = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Networking")))
        name = networking.text
        networking.click()
        return name

    def run(self,driver,domain,ip1, logger):
        name = TCP_IP_Settings().click_networking(driver)

        tcp_ip_setting = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href=\"/tcp_summary.htm\"]"))
        )
        tcp_ip_setting.click()

        NetworkIdentification = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/network_id.htm']"))
        )
        NetworkIdentification.click()



        domainName = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "IPv4_DomainName"))
        )
        domainName.clear()
        domainName.send_keys(domain)

        primaryDNSValue = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "IPv4_DnsServerId"))
        ).get_attribute("value")

        if primaryDNSValue not in ip1:
            primaryDNS = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "IPv4_DnsServerId"))
            )
            primaryDNS.clear()
            primaryDNS.send_keys(ip1)

            # Find target input and paste text
            secondaryDNS = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "IPv4_Sec_DnsServerId"))
            )
            secondaryDNS.clear()
            secondaryDNS.send_keys(primaryDNSValue)

        TCP_IP_Settings().apply(driver)
        is_succes = TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)

        tcp_ip_v6 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/tcpipv6.htm']"))
        )
        name = tcp_ip_v6.text
        tcp_ip_v6.click()

        ipv6_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[@for=\"IP6_Enable\"]")))
        if ipv6_checkbox.get_attribute('class') == 'checked':
            ipv6_checkbox.click()
        TCP_IP_Settings().apply(driver)
        is_succes &= TestSuccessMessage().test_success(driver, name, "//div[@class=\"content\"]/h2", logger)
        return is_succes