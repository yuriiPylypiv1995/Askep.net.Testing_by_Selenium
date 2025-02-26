import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from login import login_SPECIALIST_user, set_main_page, hide_phpdebugbar
from initialize_data import driver, action
from helpful_functions import switch_to_the_page_navigation


def open_amb_episodes_internal_statistic_page() -> None:
    """Функція знаходить в лівому меню профілю відповідний розділ та відкриває сторінку з меню внутрішньої статистики
    по амбулаторних епізодах"""
    internal_statistic_section = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Внутрішня статистика')]")))
    internal_statistic_section.click()

    amb_episodes_section = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Епізоди (амбулаторія)')]")))
    amb_episodes_section.click()

def open_encounters_in_episode_page(episode_name: str) -> None:
    """Функція знаходить амб епізод в переліку внутрішньої статистики (на першій сторінці), за отриманою назвою, шукає до нього кнопку перегляду взаємодій та 
    відкриває сторінку з переліком взаємодій в епізоді"""
    episode_actions_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//tr[td[text()='{episode_name}']]//button[@type='button' and contains(@class, 'v-btn') and contains(@class, 'primary--text')]")))
    action.move_to_element(episode_actions_button).perform()

    view_encounters_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'v-btn') and contains(., 'Переглянути взаємодії')]")))
    view_encounters_button.click()

def delete_encounter() -> None:
    """Функція знаходить першу невивантажену взаємодію в епізоді та видаляє її, кліком на відповідну кнопку у діях"""
    encounter_actions_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//button[@type='button' and contains(@class, 'v-btn') and contains(@class, 'primary--text')]")))
    action.move_to_element(encounter_actions_button).perform()

    delete_encounter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'v-btn') and contains(., 'Видалити взаємодію')]")))
    delete_encounter_button.click()

    confirm_delete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='Так']")))
    confirm_delete_button.click()

if __name__ == "__main__":
    # Виклики функцій для логіну користувача та підготовки головної сторінки
    login_SPECIALIST_user("specialist_nerv_cmd@askep.net", "roegpi12")
    set_main_page()

    # Виклики основних функцій скрипта
    open_amb_episodes_internal_statistic_page()
    hide_phpdebugbar()
    switch_to_the_page_navigation("3")
    open_encounters_in_episode_page("епізод для скрипта")
    delete_encounter()
    time.sleep(5)

    # Допоміжні дії для дебагу
    print("The test was executed successfully")
    # Закриття браузера
    driver.quit()
