import sys

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from faker import Faker

# Отримуємо назву файлу
script_name = sys.argv[0].split('/')[-1]

# Визначаємо URL залежно від назви файлу
urls = {
    "create_and_search_preperson.py": "https://master.devaskep.net/",
    "create_preperson.py": "https://master.devaskep.net/",
    "delete_amb_encounter.py": "https://master.devaskep.net/",
    "update_procedure.py": "https://master.devaskep.net/",
    "search_preperson.py": "https://master.devaskep.net/",

    "update_mis-token_master.py": "https://master.devaskep.net/admin/login",
    "update_mis-token_prod.py": "https://rc.askep.net/admin/login",
}

# Отримуємо URL для поточного скрипта
url = urls.get(script_name)

# Функція для встановлення масштабу через JavaScript
# def set_zoom(driver, zoom_level="80%") -> None:
#     driver.execute_script(f"document.body.style.zoom='{zoom_level}'")

# Шлях до ChromeDriver
# chrome_driver_path = '/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/chromedriver-mac-x64/chromedriver'
service = Service(port=0) # 0 означає, що буде обрано випадковий доступний порт

# Створюємо опції для Chrome
chrome_options = Options()
chrome_options.add_argument("window-size=1536,864")  # Задає розмір вікна для кращого масштабу

chrome_options.add_argument("--headless")  # запуск скриптів без графічного інтерфейсу

# Ініціалізуємо драйвер Chrome з опціями та шляхом до сервісу
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Відкриваємо веб-сторінку
driver.get(str(url))

# Створення об'єкту ActionChains
action = ActionChains(driver)
# Створення об'єкту Faker
fake = Faker('uk_UA') 
