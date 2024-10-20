import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from faker import Faker


chrome_driver_path = '/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/chromedriver-mac-x64/chromedriver'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get('https://master.devaskep.net/')

# Створення об'єкту ActionChains
action = ActionChains(driver)
# Створення об'єкту Faker
fake = Faker('uk_UA') 

# Початок скрипта тесту
main_login_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn--light-blue.btn-login")
main_login_button.click()

login_as_doctor_tab = driver.find_element(By.ID, "doctorTab")
login_as_doctor_tab.click()

# Дані для входу у профіль користувача типу SPECIALIST
login_field = driver.find_element(By.NAME, "username")
login_field.send_keys("specialist_nerv_cmd@askep.net")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("roegpi12")

login_button = driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space(text())='увійти']")
login_button.click()

time.sleep(5)

# Закриття підказок при першому вході
enjoyhint_close_btn = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CLASS_NAME, "enjoyhint_close_btn")))
action.move_to_element(enjoyhint_close_btn).perform()
action.click(enjoyhint_close_btn).perform()

# Відкриття лівого навігаційного меню
side_bar_list = driver.find_element(By.CLASS_NAME, "sitebar-list")
action.move_to_element(side_bar_list).perform()

# Приховування дебаг-панелі (phpdebugbar)
driver.execute_script("document.querySelector('.phpdebugbar').style.display = 'none';")

create_patient_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "patient-create")))
create_patient_button.click()

create_preperson_button = driver.find_element(By.XPATH, "//a[@href='https://master.devaskep.net/doctor/prepersons/create']")
create_preperson_button.click()

ok_button = driver.find_element(By.XPATH, "//button[text()='OK']")
ok_button.click()


def generate_custom_phone_number(length):
    """Генерація випадкового телефонного номера із заданою кількістю цифр"""
    phone_number = str(random.randint(0, 9))
    phone_number += ''.join(random.choices('0123456789', k=length - 1))
    return phone_number

def generate_custom_gender():
    genders = ["чоловіча", "жіноча"]
    gender = random.choice(genders)
    return str(gender)

def generate_patronymic(name: str, gender: str) -> str:
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

def get_preperson_fields():
    """Функція знаходить всі поля форми створення неідентифікованого пацієнта та повертає їх (за винятком статі та причини створення)"""
    lastname = driver.find_element(By.XPATH, "//label[text()=' Прізвище (зі слів пацієнта або супровідної особи)']/following-sibling::input")
    name = driver.find_element(By.XPATH, "//label[text()=\" Ім'я (зі слів пацієнта або супровідної особи)\"]/following-sibling::input")
    surname = driver.find_element(By.XPATH, "//label[text()=' По батькові (зі слів пацієнта або супровідної особи)']/following-sibling::input")
    birthdate = driver.find_element(By.XPATH, "//label[contains(text(), 'Дата народження (зі слів пацієнта або супровідної особи) ')]/following-sibling::input")
    
    contact_person_lastname = driver.find_element(By.XPATH, "//label[text()=' Прізвище ']/following-sibling::input")
    contact_person_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space(text())=\"Ім'я\"]/following-sibling::input")))
    contact_person_surname = driver.find_element(By.XPATH, "//label[text()=' По батькові ']/following-sibling::input")
    contact_person_mobile_phone = driver.find_element(By.XPATH, "//label[contains(text(), 'Мобільний телефон')]/following-sibling::input")
    contact_person_phone = driver.find_element(By.XPATH, "//label[contains(text(), 'Телефон стаціонарний')]/following-sibling::input")

    return (lastname, name, surname, birthdate, contact_person_lastname, contact_person_name, contact_person_surname, 
            contact_person_mobile_phone, contact_person_phone)

def fill_preperson_data(lastname, name, surname, birthdate, contact_person_lastname,
                      contact_person_name, contact_person_surname, contact_person_mobile_phone, contact_person_phone):
    """Функція заповнює всі поля форми створення неідентифікованого пацієнта"""
    time.sleep(1)
    # Приховування дебаг-панелі (phpdebugbar)
    driver.execute_script("document.querySelector('.phpdebugbar').style.display = 'none';")

    time.sleep(1)
    lastname.send_keys(fake.last_name()) 
    name.send_keys(fake.first_name())

    # Клік на контейнер, який виглядає як поле для вибору статі
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
    contact_person_surname.send_keys(generate_patronymic(str(fake.first_name()), str(generate_custom_gender())))
    contact_person_mobile_phone.send_keys(generate_custom_phone_number(10))
    contact_person_phone.send_keys(generate_custom_phone_number(10))

# Виклик основних функцій скрипта
preperson_fields = get_preperson_fields()
fill_preperson_data(*preperson_fields)

# Створення неідентифікованого пацієнта - надсилання даних на сервер та до ЦБД, кліки на відповідні кнопки
creation_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Створити')]")))
update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Оновити та вивантажити на eHealth')]")))

action.move_to_element(creation_button).perform()
creation_button.click()
time.sleep(5)
update_button.click()
time.sleep(10)

print("The test was ex ecuted successfully")

# Закриття браузера
driver.quit()
