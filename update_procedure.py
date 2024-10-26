import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from initialize_data import driver, set_zoom
from login import login_SPECIALIST_user, set_main_page, hide_phpdebugbar
from helpful_functions import scroll_page_down


def open_search_person_page() -> None:
    """Функція знаходить в лівому меню профілю відповідний розділ та відкриває сторінку пошуку ідентифікованого пацієнта,
    якому створено процедуру"""
    search_patient_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Ідентифікованого')]")
    search_patient_button.click()

def search_person(person_data: str) -> None:
    """Функція опрацьовує отримані дані пацієнта (прізвище та ім'я - обов'язково, по батькові - опційно
    вносить їх у відповідне поле для пошуку та знаходить пацієнта (через клік на клавішу Enter)"""
    person_data_input = driver.find_element(By.ID, "search_person_fullname")
    person_data_input.click()
    person_data_input.send_keys(person_data)

    # Симулюємо натискання клавіші Enter на кнопці пошуку
    search_button = driver.find_element(By.ID, "search-patient-submit")
    search_button.send_keys(Keys.ENTER)

    # Прокручуємо сторінку
    time.sleep(5)
    scroll_page_down(70)
    
# Виклики функцій для логіну користувача та підготовки головної сторінки
login_SPECIALIST_user("specialist_nerv_cmd@askep.net", "roegpi12")
set_main_page()

# Виклики основних функцій скрипта
open_search_person_page()
hide_phpdebugbar()
search_person("Тимко Андрій")
time.sleep(5)

# Допоміжні дії для дебагу
print("The test was executed successfully")
# Закриття браузера
driver.quit()
