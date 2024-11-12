import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from initialize_data import driver
from login import login_SPECIALIST_user, set_main_page, hide_phpdebugbar
from helpful_functions import generate_custom_public_id, scroll_page_down


def open_search_preperson_page(driver=driver) -> None:
    """Функція знаходить в лівому меню профілю відповідний розділ та відкриває сторінку пошуку неідентифікованого пацієнта"""
    search_patient_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Неідентифікованого')]")
    search_patient_button.click()

def search_preperson(preperson_public_id: str, driver=driver) -> None:
    """Функція опрацьовує отриманий preperson_public_id, вносить його у відповідне поле для пошуку та знаходить пацієнта"""
    preperson_public_id_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Внутрішній ідентифікатор']/following-sibling::input")))
    preperson_public_id_input.click()
    preperson_public_id_input.send_keys(preperson_public_id)

    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Шукати')]")
    search_button.click()

def view_preperson_profile(driver=driver) -> None:
    """Функція натискає на відповідну кнопку і відкриває користувачу сторінку профілю неідентифікованого пацієнта"""
    details_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Деталі')]")))
    details_button.click()
    time.sleep(30)

if __name__ == "__main__":
    # Виклики функцій для логіну користувача та підготовки головної сторінки
    login_SPECIALIST_user("specialist_nerv_cmd@askep.net", "roegpi12")
    set_main_page()

    # Виклики основних функцій скрипта
    open_search_preperson_page()
    hide_phpdebugbar()
    search_preperson(generate_custom_public_id())
    scroll_page_down(50)
    view_preperson_profile()
    scroll_page_down(70)

    # Допоміжні дії для дебагу
    print("The test was executed successfully")
    # Закриття браузера
    driver.quit()
