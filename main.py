import sys
import time
from multiprocessing import resource_tracker

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

while True:
    is_success = True
    choice = int(input("1 : EWS Configuration\n2 : Change Password\nEnter choice: "))
    if choice > 2:
        print("Wrong Choice! Please run again")
        continue
    TestSuccessMessage().delete()
    printer_ip = "10.11.13.157"  # input("Enter the printer ip address: ")
    password = "rl@12345"  # input("Enter the new password: ")
    start = time.time()
    driver = OpenEWS().run(printer_ip)
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "SettingsPages"))
        )

    except TimeoutException:
        print("Not signed in. Logging in...")
        is_success = SignUp().run(driver,password)

    if not is_success:
        print("Sign up Failed")
        driver.quit()
        # sys.exit(0)


    match choice:
        case 1:
            domain = "domain.com"  # input("Enter the domain: ")
            ip1 = "10.11.12.67"  # input("Enter the server ip address: ")
            fax_number = "722481"  # input("Enter the fax number: ")
            is_success &= SetGeneral().run(driver, ip1)
            is_success &= SetFax().run(driver, fax_number)
            is_success &= SetSecurity().run(driver, password)
            is_success &= TCP_IP_Settings().run(driver, domain, ip1)
            is_success &= Network_Settings().run(driver)
            is_success &= Other_Settings().run(driver)
            is_success &= SetWebService().run(driver, printer_ip)
            if is_success:
                print("EWS Automation Completed Successfully")
            else:
                print("EWS Automation Failed")

        case 2:
            old_password = "Rdl@12345"#input("Enter the old password: ")
            new_password = "rdl@12345"  # input("Enter the new password: ")
            if Change_Password().run(driver,old_password, new_password):
                print("Password Changed Successfully")
            else:
                print("Password Change Failed")
    time.sleep(1)
    end = time.time()
    print(f"{(end-start)//60} minutes and {(end-start)%60} seconds")
    driver.quit()
