import sys
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Change_Password import Change_Password
from Scripts.SetWebService import SetWebService
from Scripts.Networking.TCP_IP_Settings import TCP_IP_Settings
from Scripts.Networking.Other_Settings import Other_Settings
from Scripts.Networking.Network_Settings import Network_Settings
from Scripts.SetFax import SetFax
from Scripts.SetGeneral import SetGeneral
from Scripts.SetSecurity import SetSecurity
from Scripts.SignUp import SignUp
from Scripts.OpenEWS import OpenEWS
from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_store import drivers


def test(
    choice,
    printer_ip,
    password,
    domain="",
    ip1="",
    fax_number="",
    old_password="",
    new_password="",
    logger=print,
):

    is_success = True
    TestSuccessMessage().delete()
    #printer_ip = input("Enter the printer ip address: ")
    #password = input("Enter the new password: ")
    start = time.time()
    driver = OpenEWS().run(printer_ip,logger)
    drivers[printer_ip] = driver
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "SettingsPages"))
        )

    except TimeoutException:
        logger("Not signed in. Logging in...\n")
        is_success = SignUp().run(driver,password,logger)

    if not is_success:
        logger("Sign in Failed! Wrong Password\n")
        end = time.time()
        logger(f"{int((end - start) / 60)} minutes and {int((end - start) % 60)} seconds")
        driver.quit()
        return False


    match choice:
        case 1:
            #domain =  input("Enter the domain: ")
            #ip1 =  input("Enter the server ip address: ")
            #fax_number = input("Enter the fax number: ")
            logger("Executing General...\n")
            is_success &= SetGeneral().run(driver,ip1,logger)

            logger("Executing Fax...\n")
            is_success &= SetFax().run(driver, fax_number,logger)

            logger("Executing Security...\n")
            is_success &= SetSecurity().run(driver,password, logger)

            logger("Executing Networking...\n")
            is_success &= TCP_IP_Settings().run(driver,domain,ip1, logger)
            is_success &= Network_Settings().run(driver, logger)
            is_success &= Other_Settings().run(driver,logger)

            logger("Executing Webservices...\n")
            is_success &= SetWebService().run(driver,printer_ip,logger)

            if is_success:
                logger(f"EWS Automation Completed Successfully of printer {printer_ip}\n")
            else:
                logger(f"EWS Automation Failed of printer {printer_ip}\n")

        case 2:
            #old_password = input("Enter the old password: ")
            #new_password = input("Enter the new password: ")
            is_success = Change_Password().run(driver,old_password, new_password, logger)
            if is_success:
                logger(f"Password Changed Successfully of printer {printer_ip}\n")
            else:
                logger(f"Password Change Failed of printer {printer_ip}\n")
    time.sleep(1)
    end = time.time()
    logger(f"{int((end-start)/60)} minutes and {int((end-start)%60)} seconds\n")
    driver.quit()
    return True

if __name__ == "__main__":
    test()
