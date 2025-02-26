from initialize_data import driver
from login import hide_phpdebugbar, set_main_page, login_SPECIALIST_user
from helpful_functions import scroll_page_down

from create_preperson import open_create_preperson_form, get_preperson_fields, fill_preperson_data, create_preperson, get_preperson_public_id
from search_preperson import view_preperson_profile, open_search_preperson_page, search_preperson


if __name__ == "__main__":
    # Виклики функцій для логіну користувача та підготовки головної сторінки
    login_SPECIALIST_user("info+specialist_nerv_cmd@askep.net", "roegpi12")
    set_main_page()

    # Виклики основних функцій скрипта
    open_create_preperson_form()
    preperson_fields = get_preperson_fields()
    fill_preperson_data(*preperson_fields)
    create_preperson()

    preperson_public_id = get_preperson_public_id()
    set_main_page()

    open_search_preperson_page()
    hide_phpdebugbar()
    search_preperson(preperson_public_id)
    scroll_page_down(50)
    view_preperson_profile()
    scroll_page_down(100)

    # Допоміжні дії для дебагу
    print(preperson_public_id)
    print("The test was executed successfully") 
    # Закриття браузера
    driver.quit()
