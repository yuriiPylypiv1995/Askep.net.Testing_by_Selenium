import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from initialize_data import driver, action
from login import login_SPECIALIST_user, set_main_page, hide_phpdebugbar
from helpful_functions import scroll_page_down, scroll_modal_patient_menu, switch_to_the_last_tab


def open_search_person_page() -> None:
    """Функція знаходить в лівому меню профілю відповідний розділ та відкриває сторінку пошуку ідентифікованого пацієнта,
    якому створено процедуру"""
    search_patient_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Ідентифікованого')]")))
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
    time.sleep(3)
    scroll_page_down(70)

def open_patient_procedures_page(data_id: str) -> None:
    """Функція відкриває сторінку з переліком процедур по ідентифікованому пацієнту"""
    patient_menu_button = driver.find_element(By.XPATH, f"//a[@data-id='{data_id}' and text()='Дії']")
    patient_menu_button.click()

    scroll_modal_patient_menu()

    procedures_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Процедури')]")))
    procedures_button.click()

def open_procedure_edit_page(procedure_id: str) -> None:    
    """Функція знаходить процедуру в переліку за отриманим procedure_id, шукає до неї кнопку редагування та 
    відкриває сторінку редагування процедури"""
    time.sleep(40)
    switch_to_the_last_tab()
    hide_phpdebugbar()
    scroll_page_down(90)

    procedure_actions_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, f"//tr[td[text()='{procedure_id}']]//ul[@data-tipsinfo='Actions button']//li")))
    action.move_to_element(procedure_actions_button).perform()

    edit_procedure_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), 'Редагувати') and @href='/doctor/procedures/{procedure_id}']")))
    edit_procedure_button.click()

# Виклики функцій для логіну користувача та підготовки головної сторінки
login_SPECIALIST_user("specialist_nerv_cmd@askep.net", "roegpi12")
set_main_page()

# Виклики основних функцій скрипта
open_search_person_page()
hide_phpdebugbar()
search_person("Тимко Андрій")
time.sleep(2)
open_patient_procedures_page("960056")
open_procedure_edit_page("9064")
time.sleep(10)

# Допоміжні дії для дебагу
print("The test was executed successfully")
# Закриття браузера
driver.quit()
