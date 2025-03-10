from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from faker import Faker


# Функція для встановлення масштабу через JavaScript
# def set_zoom(driver, zoom_level="80%") -> None:
#     driver.execute_script(f"document.body.style.zoom='{zoom_level}'")

# Шлях до ChromeDriver
# chrome_driver_path = '/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/chromedriver-mac-x64/chromedriver'
service = Service(port=0) # 0 означає, що буде обрано випадковий доступний порт

# Створюємо опції для Chrome
chrome_options = Options()
chrome_options.add_argument("window-size=1536,864")  # Задає розмір вікна для кращого масштабу
# chrome_options.add_argument("--headless")  # запуск скриптів без графічного інтерфейсу

# Ініціалізуємо драйвер Chrome з опціями та шляхом до сервісу
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Відкриваємо веб-сторінку
driver.get('https://master.devaskep.net/')

# Створення об'єкту ActionChains
action = ActionChains(driver)
# Створення об'єкту Faker
fake = Faker('uk_UA') 
