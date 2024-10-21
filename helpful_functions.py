import random


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
