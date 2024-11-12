import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from initialize_data import driver


def generate_custom_phone_number(length: int) -> str:
    """Генерація випадкового телефонного номера із заданою кількістю цифр"""
    phone_number = str(random.randint(0, 9))
    phone_number += ''.join(random.choices('0123456789', k=length - 1))
    return phone_number

def generate_custom_gender() -> str:
    genders = ["чоловіча", "жіноча"]
    gender = random.choice(genders)
    return str(gender)

def generate_custom_patronymic(name: str, gender: str) -> str:
    """Генерація випадкового по батькові, на основі комбінації заданого імені та статі"""
    # Обрізаємо можливі пробіли
    name = name.strip().lower()

    # Остання літера імені
    last_letter = name[-1]

    if gender == 'чоловіча':
        # Для чоловічих по батькові
        if last_letter in ['а', 'я', 'й', 'ь']:
            patronymic = name[:-1] + "йович"  # Якщо на голосну або м'який приголосний
        else:
            patronymic = name + "ович"  # Якщо на твердий приголосний
    elif gender == 'жіноча':
        # Для жіночих по батькові
        if last_letter in ['а', 'я', 'й', 'ь']:
            patronymic = name[:-1] + "ївна"  # Якщо на голосну або м'який приголосний
        else:
            patronymic = name + "івна"  # Якщо на твердий приголосний
    else:
        raise ValueError("Невідома стать, використовуйте 'чоловіча' або 'жіноча'.")
    
    # Повертаємо по батькові з великої літери
    return patronymic.capitalize()

def generate_custom_public_id() -> str:
    """Генерація штучного публічного ідентифікатора існуючого в базі неідентифікованого пацієнта"""
    id = random.choice(range(2000, 2211))
    return str(id)

def scroll_page_down(percent_to_scroll: int, driver=driver) -> None:
    """Прокрутка сторінки донизу на задану кількість відсотків"""
    # Отримати висоту всього документа та висоту вікна (показуваного контенту)
    document_height = driver.execute_script("return document.body.scrollHeight")
    window_height = driver.execute_script("return window.innerHeight")

    # Обчислити, на скільки пікселів прокрутити
    pixels_to_scroll = (document_height - window_height) * (percent_to_scroll / 100)

    # Прокрутка на обчислену кількість пікселів
    driver.execute_script(f"window.scrollTo(0, {pixels_to_scroll});")

def scroll_page_up(percent_to_scroll: int, driver=driver) -> None:
    """Прокрутка сторінки догори на задану кількість відсотків"""
    # Отримати висоту всього документа та висоту вікна (показуваного контенту)
    document_height = driver.execute_script("return document.body.scrollHeight")
    window_height = driver.execute_script("return window.innerHeight")

    # Обчислити, на скільки пікселів прокрутити
    pixels_to_scroll = (document_height - window_height) * (percent_to_scroll / 100)

    # Прокрутка на обчислену кількість пікселів догори
    driver.execute_script(f"window.scrollBy(0, -{pixels_to_scroll});")

def scroll_modal_patient_menu(driver=driver) -> None:
    """Прокрутка модального вікна меню ідентифікованого павцієнта донизу"""
    # Знаходимо елемент modal-body
    modal_body = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                                "//div[contains(@class, 'modal-body') and .//h5[text()=' Виписати без заповнення всієї історії']]")))

    # Прокручуємо модальне вікно до самого низу
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_body)

def switch_to_the_last_tab(driver=driver) -> None:
    """Функція перемикає драйвер на останню відкриту вкладку в браузері"""
    driver.switch_to.window(driver.window_handles[-1])  # Перемикаємося на останню вкладку

def get_page_source(driver=driver) -> None:
    """Отримуємо HTML-код сторінки та записуємо його у файл"""
    page_html = driver.page_source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(page_html)

def switch_to_the_page_navigation(page_num: str, driver=driver) -> None:
    """Переключення на задану сторінку, якщо передбачена пагінація.
    ! Функція писалася під сторінку з переліком амбулаторних епізодів у внутрішній статистиці"""
    navigation_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='Перейти на сторінку {str(page_num)}']")))
    navigation_button.click()
