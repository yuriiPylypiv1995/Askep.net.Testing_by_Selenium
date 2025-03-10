import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from initialize_data import driver
from login import login_ADMIN_user, set_main_ADMIN_page

def ehealth_auth(ehealth_login: str, ehealth_password: str) -> None:
    """Функція відкриває інтерфейс ehealth, вводить дані для авторизації і натискає кнопку для 
    їх надсилання """
    eHealth_oAuth_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='https://rc.askep.net/ehealth/oauth']")))
    eHealth_oAuth_button.click()

    get_access_token_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Отримати Access Token')]")))
    get_access_token_button.click()

    # ehealth_login_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    # ehealth_login_field.send_keys(ehealth_login)

    ehealth_pass_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    ehealth_pass_field.send_keys(ehealth_password)
    
    submit_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div/button[@type='submit' and text()='увійти']")))
    # submit_button.click()
    driver.execute_script("arguments[0].click();", submit_button)
    time.sleep(1)

    approve_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[button[normalize-space()='прийняти та продовжити']]")))
    approve_button.click()
    time.sleep(3)

    # continue_button = WebDriverWait(driver, 10).until(
    # EC.presence_of_element_located((By.XPATH, "//button//*[text()='продовжити']")))
    # continue_button.click()

if __name__ == "__main__":
    # Виклики функцій для логіну користувача та підготовки головної сторінки
    login_ADMIN_user("superadmin@askep.net", "8tXd6J8pG6")
    set_main_ADMIN_page()

    # Виклики основних функцій скрипта
    ehealth_auth("info@askep.net", "pJoA8w3mDE&ja;d4BiM616")

    # Допоміжні дії для дебагу
    print("The test was executed successfully")
    # Закриття браузера
    driver.quit()
