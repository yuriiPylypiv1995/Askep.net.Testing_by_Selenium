import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from initialize_data import driver, fake, action
from login import hide_phpdebugbar, login_SPECIALIST_user, set_main_page
from helpful_functions import generate_custom_gender, generate_custom_patronymic, generate_custom_phone_number


def open_create_preperson_form() -> None:
    """Функція знаходить у лівому меню профілю відповідний розділ та відкриває форму створення неідентифікованого пацієнта"""
    create_patient_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "patient-create")))
    create_patient_button.click()

    create_preperson_button = driver.find_element(By.XPATH, "//a[@href='https://master.devaskep.net/doctor/prepersons/create']")
    create_preperson_button.click()

    ok_button = driver.find_element(By.XPATH, "//button[text()='OK']")
    ok_button.click()

def get_preperson_fields() -> tuple:
    """Функція знаходить всі поля форми створення неідентифікованого пацієнта та повертає їх (за винятком статі та причини створення)"""
    # Дані пацієнта
    lastname = driver.find_element(By.XPATH, "//label[text()=' Прізвище (зі слів пацієнта або супровідної особи)']/following-sibling::input")
    name = driver.find_element(By.XPATH, "//label[text()=\" Ім'я (зі слів пацієнта або супровідної особи)\"]/following-sibling::input")
    surname = driver.find_element(By.XPATH, "//label[text()=' По батькові (зі слів пацієнта або супровідної особи)']/following-sibling::input")
    birthdate = driver.find_element(By.XPATH, "//label[contains(text(), 'Дата народження (зі слів пацієнта або супровідної особи) ')]/following-sibling::input")
    
    # Дані контактної особи
    contact_person_lastname = driver.find_element(By.XPATH, "//label[text()=' Прізвище ']/following-sibling::input")
    contact_person_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())=\"Ім'я\"]/following-sibling::input")))
    contact_person_surname = driver.find_element(By.XPATH, "//label[text()=' По батькові ']/following-sibling::input")
    contact_person_mobile_phone = driver.find_element(By.XPATH, "//label[contains(text(), 'Мобільний телефон')]/following-sibling::input")
    contact_person_phone = driver.find_element(By.XPATH, "//label[contains(text(), 'Телефон стаціонарний')]/following-sibling::input")

    return (lastname, name, surname, birthdate, contact_person_lastname, contact_person_name, contact_person_surname, 
            contact_person_mobile_phone, contact_person_phone)

def fill_preperson_data(lastname: WebElement, name: WebElement, surname: WebElement, birthdate: WebElement, contact_person_lastname: WebElement,
                      contact_person_name: WebElement, contact_person_surname: WebElement, contact_person_mobile_phone: WebElement, contact_person_phone: WebElement) -> None:
    """Функція заповнює всі поля форми створення неідентифікованого пацієнта."""
    time.sleep(1)
    hide_phpdebugbar()
    time.sleep(1)

    lastname.send_keys(fake.last_name()) 
    name.send_keys(fake.first_name())

    # Клік на контейнер, який є полем для вибору статі
    gender = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='select2-selection select2-selection--single']")))
    gender.click()
    # Вибір випадкової опції з відкритого списку
    gender_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{generate_custom_gender()}')]")))
    gender_option.click()
    # Отримання тексту з контейнера, який відображає вибрану стать після вибору
    gender_container_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='select2-selection__rendered']"))).text

    if gender_container_text == "чоловіча":
        surname.send_keys("Батькович")
    else:
         surname.send_keys("Батьківна")

    birthdate.send_keys(fake.date_of_birth().strftime("%d.%m.%Y")) # type: ignore

    # Робота із випадаючим списком Select2 причини створення неідентифікованого пацієнта
    # Крок 1: Клік на контейнер Select2 для відкриття списку причин
    creation_reason = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'select2-selection__rendered') and .//span[text()='Виберіть причину']]")))
    creation_reason.click()
    # Крок 2: Клік на контейнер Select2 для вибору причини зі списку
    reason_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'form-group')]/label[text()='Причина створення неідентифікованого пацієнта ']/following-sibling::div//span[@class='select2-selection select2-selection--single']")))
    reason_container.click()
    # Крок 3: Знаходження причини, яку потрібно вибрати
    desired_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Інші обставини звернення для госпіталізації')]")))
    desired_option.click()
    # Крок 4: Клік на вибрану причину для того щоб закрити список
    desired_li = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Інші обставини звернення для госпіталізації')]")))
    desired_li.click()

    # Очікування появи поля "Примітки" 
    notes = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Примітки')]/following-sibling::textarea")))
    notes.send_keys("Тестовий текст приміток")

    # Заповнення даних контактної особи
    contact_person_lastname.send_keys(fake.last_name())
    contact_person_name.send_keys(fake.first_name())
    contact_person_surname.send_keys(generate_custom_patronymic(str(fake.first_name()), str(generate_custom_gender())))
    contact_person_mobile_phone.send_keys(generate_custom_phone_number(10))
    contact_person_phone.send_keys(generate_custom_phone_number(10))

def create_preperson() -> None:
    """Функція створює неідентифікованого пацієнта - надсилає дані на сервер та до ЦБД, виконуючи кліки на відповідні кнопки"""
    creation_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Створити')]")))
    update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Оновити та вивантажити на eHealth')]")))

    action.move_to_element(creation_button).perform()
    creation_button.click()
    time.sleep(5)
    update_button.click()
    time.sleep(10)

def get_preperson_public_id() -> str | None:
    """Функція повертає публічний ідентифікатор створеного та вивантаженого до ЦБД неідентифікованого пацієнта. 
       Приклад: 41571077.3329002795.2197"""
    # Знайти елемент за назвою
    label_element = driver.find_element(By.XPATH, "//label[text()=' Ідентифікатор пацієнта ']")
    # Якщо знайдено, шукаємо input поруч
    input_element = label_element.find_element(By.XPATH, "./following-sibling::input")
    # Отримати значення поля
    value = input_element.get_attribute('value')
    return value

# Виклики основних функцій скрипта
login_SPECIALIST_user("specialist_nerv_cmd@askep.net", "roegpi12")
set_main_page()
open_create_preperson_form()
preperson_fields = get_preperson_fields()
fill_preperson_data(*preperson_fields)
create_preperson()

# Допоміжні дії для дебагу
print(get_preperson_public_id())
print("The test was executed successfully")
# Закриття браузера
driver.quit()
