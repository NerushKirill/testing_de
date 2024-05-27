import sys
from pprint import pprint
from src.DataProvider.DataProviderDB import save_user, get_chek_email, get_users_db, update_param_table_cities_db, \
    update_param_table_locations_db, update_param_table_registration_data_db, update_param_table_media_data_db, \
    update_param_table_contact_details_db, update_param_table_users_db
from src.DataProvider.DataProviderURl import parsing_json_file, get_user_url
from src.resources.constants import update_attr

url = "https://randomuser.me/api/?results="


def get_url():
    return url


def set_url(new_url):
    global url
    url = new_url


def add_users():
    count_user_in_db = 0
    exit_add = True
    while exit_add:
        try:
            count = int(input("введите количество пользователей: "))
            if type(int(count)) == int:
                for num in range(count):
                    json_file = get_user_url(num, url)
                    if len(json_file) != 0:
                        pars_json = parsing_json_file(json_file)
                        pprint(pars_json)
                        count_user_in_db += save_user(pars_json)
                print("Успешно добавлено: ", count_user_in_db, "записей")
            exit_add = False
        except ValueError:
            print("ОШИБКА: ведите число:  ")


def change_url():
    new_url = input("введите корректный url: ")
    set_url(new_url)
    print("\n url изменен \n", get_url())


def get_invalid_users():
    results = get_users_db(False)
    if len(results) != 0:
        for row in results:
            print(", ".join(map(str, row)))
    else:
        print("нет таких записей")


def get_valid_users():
    results = get_users_db(True)
    if len(results) != 0:
        for row in results:
            print(", ".join(map(str, row)))
    else:
        print("нет таких записей\n")


def email_check():
    email: str = input("введите email:")
    answer_email: list = get_chek_email(email)
    if len(answer_email) == 0:
        print("нет такого email в базе\n")
    else:
        print("есть такой email в базе\n")


def update_param():
    print(*[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep='\n')
    num_param = input("выберите параметр на изменение:")
    try:
        options = list(update_attr.keys())
        selected_key = options[int(num_param) - 1]
        print("Вы выбрали параметр:", selected_key)

        value = input("На что поменять: ")
        email_user = input("Выберете пользователя по email: ")

        select_table = update_attr.get(selected_key)
        print(select_table[0])
        if select_table[0] == 'cities':
            update_param_table_cities_db(email_user, selected_key, value)
        elif select_table[0] == 'contact_details':
            update_param_table_contact_details_db(email_user, selected_key, value)
        elif select_table[0] == 'locations':
            update_param_table_locations_db(email_user, selected_key, value)
        elif select_table[0] == 'media_data':
            update_param_table_media_data_db(email_user, selected_key, value)
        elif select_table[0] == 'registration_data':
            update_param_table_registration_data_db(email_user, selected_key, value)
        elif select_table[0] == 'users':
            update_param_table_users_db(email_user, selected_key, value)
        print(email_user, selected_key, value, update_attr.get(selected_key))

        #update_param_db(email_user, update_attr.get(selected_key), value)
    except (ValueError, IndexError):
        print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(options))


def exit_program():
    sys.exit()
