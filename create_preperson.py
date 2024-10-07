import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_driver_path = '/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/chromedriver-mac-x64/chromedriver'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get('https://master.devaskep.net/')

# Створення об'єкту ActionChains
action = ActionChains(driver)

main_login_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn--light-blue.btn-login")
main_login_button.click()

login_as_doctor_tab = driver.find_element(By.ID, "doctorTab")
login_as_doctor_tab.click()

login_field = driver.find_element(By.NAME, "username")
login_field.send_keys("specialist_nerv_cmd@askep.net")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("roegpi12")

login_button = driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space(text())='увійти']")
login_button.click()

time.sleep(30)

enjoyhint_close_btn = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CLASS_NAME, "enjoyhint_close_btn")))
action.move_to_element(enjoyhint_close_btn).perform()
action.click(enjoyhint_close_btn).perform()

side_bar_list = driver.find_element(By.CLASS_NAME, "sitebar-list")
action.move_to_element(side_bar_list).perform()

# Приховуємо дебаг-панель (phpdebugbar)
driver.execute_script("document.querySelector('.phpdebugbar').style.display = 'none';")

create_patient_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "patient-create")))
create_patient_button.click()
time.sleep(2)

create_preperson_button = driver.find_element(By.XPATH, "//a[@href='https://master.devaskep.net/doctor/prepersons/create']")
create_preperson_button.click()

print("The test was executed successfully")
time.sleep(10)

# # Закриття браузера
# driver.quit()
