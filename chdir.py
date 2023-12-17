from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fill_form(times_to_fill):
    try:
        # Set up the driver
        driver = webdriver.Firefox(executable_path='geckodriver')

        for _ in range(times_to_fill):
            # Open the webpage
            driver.get('https://divar.ir/chat')

            submit_elem =  driver.element = driver.find_element_by_class_name('kt-button.kt-button--primary')
            submit_elem.click()
            time.sleep(3)
            # Locate the form elements and fill them out
            
            # Fill the phone number field
            # Finding element by class name
            #phone_elem = driver.element = driver.find_element_by_class_name('kt-textfield .kt-textfield__input')
            #phone_elem.send_keys('09177723977')
            #element = driver.find_element_by_css_selector('input[placeholder="شمارهٔ موبایل"]')
            element = driver.find_element_by_class_name('kt-textfield__input')
            #wait = WebDriverWait(driver, 30)  # Wait up to 10 seconds
            element.send_keys('09173761545')
            time.sleep(3)
   
            
            # Submit the form using a single, unique class from the list of classes
            submit_elem =  driver.element = driver.element = driver.find_element_by_class_name('kt-button.kt-button--primary')
            submit_elem.click()
            


            actions = ActionChains(driver)
            actions.move_to_element(submit_elem).click().perform()
            # Wait for a few seconds before filling the form again
            driver.refresh()
            time.sleep(5)

        driver.close()
    
    except Exception as e:
        print("An error occurred:", e)
        if driver:
            driver.quit()

# Call the function
fill_form(60)
