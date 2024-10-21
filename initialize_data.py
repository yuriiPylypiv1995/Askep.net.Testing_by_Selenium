from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from faker import Faker


chrome_driver_path = '/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/chromedriver-mac-x64/chromedriver'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.get('https://master.devaskep.net/')

# Створення об'єкту ActionChains
action = ActionChains(driver)
# Створення об'єкту Faker
fake = Faker('uk_UA') 
