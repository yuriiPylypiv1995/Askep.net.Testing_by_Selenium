import time
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse, parse_qs

from initialize_data import driver
from login import login_ADMIN_user, set_main_ADMIN_page
from logging_config_master import logging

def ehealth_auth(ehealth_login: str, ehealth_password: str) -> None:
    """Функція відкриває інтерфейс ehealth, вводить дані для авторизації і натискає кнопку для 
    їх надсилання """
    eHealth_oAuth_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='https://master.devaskep.net/ehealth/oauth']")))
    eHealth_oAuth_button.click()

    get_access_token_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Отримати Access Token')]")))
    get_access_token_button.click()

    # ehealth_login_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    # ehealth_login_field.send_keys(ehealth_login)

    ehealth_pass_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    ehealth_pass_field.send_keys(ehealth_password)
    
    submit_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button//*[text()='Увійти']")))
    submit_button.click()

    approve_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button//*[text()='Прийняти та продовжити']")))
    approve_button.click()
    time.sleep(1)

    # continue_button = WebDriverWait(driver, 10).until(
    # EC.presence_of_element_located((By.XPATH, "//button//*[text()='продовжити']")))
    # continue_button.click()

def get_access_token():
    """Ця функція виділяє з url спеціальний набір символів, повертається назад в адмінку і переходить за потрібним
    посиланням"""
    # Отримуємо поточний URL сторінки
    current_url = driver.current_url

    # Використовуємо urlparse для парсингу URL
    parsed_url = urlparse(current_url)

    # Отримуємо параметри запиту після знака "?"
    query_params = parse_qs(parsed_url.query)

    code_value = query_params.get('code', [None])[0]
    formatted_url = f"?code={code_value}"

    # Повертаємось на три кроки назад
    for _ in range(3):
        driver.back()
        time.sleep(1)

    driver.get(f"https://master.devaskep.net/ehealth/oauth{formatted_url}")
    time.sleep(3)

if __name__ == "__main__":
    try:
        # Виклики функцій для логіну користувача та підготовки головної сторінки
        login_ADMIN_user("superadmin@askep.net", "kDBSCGTN")
        set_main_ADMIN_page()

        # Виклики основних функцій скрипта
        ehealth_auth("mis_dbf51fee31@email.com", "3%%uZmf2&9v_bO?Tx&25")
        get_access_token()

        # Допоміжні дії для дебагу
        logging.info("The test was executed successfully")
        # Закриття браузера
        driver.quit()
    except Exception:
        logging.error(traceback.format_exc())  # Логування повного traceback
