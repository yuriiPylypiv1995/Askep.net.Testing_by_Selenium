import logging


# Налаштування логування
logging.basicConfig(
    filename="/Users/VisualStudioCodeProjects/Askep.net.Testing_by_Selenium/logs_master.log",  # Ім'я файлу для логів
    level=logging.INFO,  # Рівень логування (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат повідомлення
    datefmt="%Y-%m-%d %H:%M:%S",  # Формат дати й часу
)

# Створюємо логер, щоб можна було його використовувати в інших модулях
logger = logging.getLogger(__name__)
