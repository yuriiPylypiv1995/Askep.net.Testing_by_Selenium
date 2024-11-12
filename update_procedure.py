import time
import random
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from initialize_data import driver, action, fake
from login import login_SPECIALIST_user, set_main_page, hide_phpdebugbar
from helpful_functions import scroll_page_down, scroll_modal_patient_menu, switch_to_the_last_tab, scroll_page_up


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
    switch_to_the_last_tab()
    hide_phpdebugbar()
    scroll_page_down(90)

    procedure_actions_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//tr[td[text()='{procedure_id}']]//ul[@data-tipsinfo='Actions button']//li")))
    action.move_to_element(procedure_actions_button).perform()

    edit_procedure_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), 'Редагувати') and @href='/doctor/procedures/{procedure_id}']")))
    edit_procedure_button.click()

def update_procedure() -> None:
    """Функція редагує три поля форми виконаної процедури, а саме: Результат проведення процедури,
    Нотатки та Дата паперового скерування *"""
    hide_phpdebugbar()
    scroll_page_down(30)

    procedure_results = ["Інше", 
                         "Процедура проведена успішно", 
                         "Проведення процедури не завершено: ускладнення, які виникли в процесі процедури",
                         "Проведення процедури не завершено: пацієнт відмовився від продовження процедури",
                         "Проведення процедури не завершено: технічні проблеми",
                         "Процедура проведена не успішно",
                         ]
    procedure_results_selected = random.choice(procedure_results)

    # Створюємо умову XPath з "or" для кожного значення
    xpath_condition = " or ".join([f"@title='{result}'" for result in procedure_results])
    
    # Клік на контейнер Select2 для відкриття списку
    procedure_result_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='select2-selection__rendered' and @id='select2--container' and @role='textbox' and ({xpath_condition})]")))
    procedure_result_field.click()

    # Знаходження рандомного результату, який потрібно вибрати
    desired_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//option[contains(text(), '{procedure_results_selected}')]")))
    desired_result.click()

    # Крок 4: Клік на вибрану причину для того щоб закрити список
    desired_li = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{procedure_results_selected}')]")))
    desired_li.click()

    notes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-group ']/textarea")))
    notes.clear()
    notes.send_keys(fake.text(max_nb_chars=100))

    scroll_page_down(50)

    paper_refferal_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-group']//div[@class='input-group  working_hours']//input[@type='text']")))
    paper_refferal_date.clear()
    start_date = date(2017, 1, 1)
    end_date = date(2024, 11, 5)
    paper_refferal_date.send_keys(fake.date_between(start_date=start_date, end_date=end_date).strftime("%d-%m-%Y %H:%M")) # type: ignore

def save_procedure() -> None:
    """Функція зберігає оновлену процедуру, знаходячи та натиснувши на відповідну кнопку у формі"""
    scroll_page_up(100)
    update_procedure_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Оновити процедуру')]")))
    update_procedure_button.click()

if __name__ == "__main__":
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
    update_procedure()
    save_procedure()
    time.sleep(10)

    # Допоміжні дії для дебагу
    print("The test was executed successfully")
    # Закриття браузера
    driver.quit()
