import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


from initialize_data import driver, action

def login_SPECIALIST_user(login: str, password: str, driver=driver) -> None:
    """Функція знаходить потрібні елементи та залогінює користувача типу SPECIALIST за наданими логіном та паролем"""
    main_login_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn--light-blue.btn-login")
    main_login_button.click()

    login_as_doctor_tab = driver.find_element(By.ID, "doctorTab")
    login_as_doctor_tab.click()

    # Дані для входу у профіль користувача типу SPECIALIST
    login_field = driver.find_element(By.NAME, "username")
    login_field.send_keys(login)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space(text())='увійти']")
    login_button.click()

    time.sleep(5)

def login_ADMIN_user(login: str, password: str, driver=driver) -> None:
    """Функція знаходить потрібні елементи та залогінює адміна за наданими логіном та паролем"""
    login_field = driver.find_element(By.ID, "email")
    login_field.send_keys(login)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[span[contains(text(), 'Вхід')]]")
    login_button.click()

def hide_phpdebugbar(driver=driver) -> None:
    """Функція приховує нижню дебаг-панель, щоб вона не заважала знаходити елементи на сторінці"""
    driver.execute_script("document.querySelector('.phpdebugbar').style.display = 'none';")

def set_main_page(driver=driver) -> None:
    """Функція очищає головну сторінку профілю залогіненого користувача від зайвих веб-елементів"""
    # Закриття підказок при першому вході
    # enjoyhint_close_btn = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CLASS_NAME, "enjoyhint_close_btn")))
    # action.move_to_element(enjoyhint_close_btn).perform()
    # action.click(enjoyhint_close_btn).perform()

    # Відкриття лівого навігаційного меню
    side_bar_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sitebar-list")))
    action.move_to_element(side_bar_list).perform()

    # Cкролити до розділу "Пацієнти" -> "Пошук пацієнта" -> "Неідентифікованого"
    search_patient_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Неідентифікованого')]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", search_patient_button)

    hide_phpdebugbar()

def set_main_ADMIN_page(driver=driver) -> None:
    """Функція налаштовує головну сторінку в адмінці для подальшої роботи (розгортає боковий сайтбар та
    шукає потрібний для авторизації на eHealth розділ)"""
    hide_phpdebugbar()

    # Відкриття лівого навігаційного меню
    side_bar_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "side-menu-container")))
    action.move_to_element(side_bar_list).perform()

    # Cкролити до розділу "eHealth і відкрити його"
    # Отримуємо поточний URL сторінки
    current_url = driver.current_url

    if current_url == "https://master.devaskep.net/admin":
        ehealth_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='https://master.devaskep.net/admin/ehealth']/span[text()='eHealth']"))
    )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ehealth_link)
        ehealth_link.click()
    else:
        ehealth_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='https://rc.askep.net/admin/ehealth']/span[text()='eHealth']"))
    )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ehealth_link)
        ehealth_link.click()
