import random

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
    id = random.choice(range(1, 2202))
    return str(id)

def scroll_page_down(percent_to_scroll: int) -> None:
    """Прокрутка сторінки донизу на задану кількість відсотків"""
    # Отримати висоту всього документа та висоту вікна (показуваного контенту)
    document_height = driver.execute_script("return document.body.scrollHeight")
    window_height = driver.execute_script("return window.innerHeight")

    # Обчислити, на скільки пікселів прокрутити
    pixels_to_scroll = (document_height - window_height) * (percent_to_scroll / 100)

    # Прокрутка на обчислену кількість пікселів
    driver.execute_script(f"window.scrollTo(0, {pixels_to_scroll});")
