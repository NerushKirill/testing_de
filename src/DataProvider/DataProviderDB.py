from datetime import datetime
from pathlib import Path
import psycopg2
from psycopg2 import OperationalError, ProgrammingError, DatabaseError
from src.resources import constants
from src.validators.validator_email import validator_email
from src.validators.validator_password import validator_password


def connect_db(query):
    try:
        connection = psycopg2.connect(
            host=constants.HOST,
            user=constants.USER,
            password=constants.PASSWORD,
            database=constants.DB
        )
    except UnboundLocalError as ue:
        print(f"Ошибка connection: {ue}")
    except OperationalError as oe:
        print(f"Ошибка подключения к базе данных: {oe}")

    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

            if cursor.description is not None:
                return cursor.fetchall()
            else:
                return False
    except psycopg2.errors.UniqueViolation as e:
        print(f"Ошибка уникального ограниченияe: {e} Данные не будут добавлены")

    except ProgrammingError as pe:
        if str(pe) != 'Ошибка:  отношение "contact_details" уже существует\n':
            print(f"Ошибка в SQL запросе: {pe}")
    except DatabaseError as de:
        print(f"Ошибка базы данных: {de}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def create_db():
    query = """
    SELECT COUNT(*) FROM pg_catalog.pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema'); """

    count_table = connect_db(query)

    if count_table[0][0] == 0:
        current_file_path = Path(__file__).resolve()
        project_root = current_file_path.parents[2]
        sql_path = project_root / 'docs' / 'sql' / 'DDL.sql'
        print(sql_path)
        try:
            with open(sql_path, 'r') as file:
                sql_script = file.read()
            connect_db(sql_script)
        except FileNotFoundError as fe:
            print(f"Ошибка пути: {fe}")


def save_user(data_dict):
    if validator_email(data_dict['email']):
        print("email валиден")
    else:
        print("email не валиден")

    query = """
            INSERT INTO cities(city, state, country, created_dttm, updated_dttm)
            VALUES ('{}', '{}', '{}','{}','{}')
            RETURNING city_id
        """.format(
        data_dict['city'],
        data_dict['state'],
        data_dict['country'],
        datetime.now(),
        datetime.now()
    )

    city = connect_db(query)

    if city:
        city_id = city[0][0]
        query = """INSERT INTO users(gender, name_title, name_first, name_last, age, nat, created_dttm, updated_dttm) 
        VALUES ('{}','{}','{}','{}',{},'{}','{}','{}')RETURNING user_id """.format(data_dict['gender'],
                                                                                   data_dict['name_title'],
                                                                                   data_dict['name_first'],
                                                                                   data_dict['name_last'],
                                                                                   data_dict['age'], data_dict['nat'],
                                                                                   datetime.now(), datetime.now())

        user = connect_db(query)
        user_id: int = user[0][0]

        query = """INSERT INTO contact_details (user_id, phone, cell, created_dttm, updated_dttm)
        VALUES ({}, '{}', '{}','{}','{}')""".format(user_id, data_dict["phone"], data_dict["cell"], datetime.now(),
                                                    datetime.now())

        connect_db(query)

        query = """
        INSERT INTO media_data(user_id, picture, created_dttm, updated_dttm)
        VALUES ({}, '{}', '{}','{}')""".format(user_id, data_dict['picture'], datetime.now(), datetime.now())

        connect_db(query)

        query = """
            INSERT INTO registration_data (user_id, email, username, password, password_md5, password_validation, 
            created_dttm, updated_dttm)
            VALUES ({}, '{}', '{}','{}','{}', {}, '{}','{}')""".format(
            user_id,
            data_dict['email'],
            data_dict['username'],
            data_dict['password'],
            data_dict['password_md5'],
            validator_password(data_dict['password']),  # Пример значения для password_validation
            datetime.now(),
            datetime.now()
        )

        connect_db(query)

        query = """
            INSERT INTO locations (user_id, city_id, street_name, street_number, postcode, latitude, longitude, 
            created_dttm, updated_dttm)
            VALUES ({}, {}, '{}',{},'{}',{}, {}, '{}','{}')""".format(
            user_id,
            city_id,
            data_dict['street_name'],
            data_dict['street_number'],
            data_dict['postcode'],
            data_dict['latitude'],
            data_dict['longitude'],
            datetime.now(),
            datetime.now()
        )

        connect_db(query)
        return 1
    return 0


def get_users_db(param: bool):
    query = """SELECT * FROM users     
    JOIN contact_details ON users.user_id = contact_details.user_id 
    JOIN media_data ON users.user_id = media_data.user_id 
    JOIN registration_data ON users.user_id = registration_data.user_id
    JOIN locations ON users.user_id = locations.user_id
    WHERE registration_data.password_validation = {}""".format(param)
    return connect_db(query)


def get_chek_email(email: str):
    query = """SELECT * FROM REGISTRATION_DATA WHERE EMAIL = '{}'""".format(email)
    return connect_db(query)


def update_param_table_locations_db(email, name_param, value):
    query = """UPDATE locations SET {} = '{}' WHERE
            user_id = (SELECT user_id FROM registration_data WHERE email = '{}')""".format(name_param, value, email)
    connect_db(query)


def update_param_table_cities_db(email, name_param, value):
    query = """UPDATE cities SET {} = '{}' WHERE city_id = (SELECT city_id FROM locations WHERE user_id = (SELECT 
            user_id FROM registration_data WHERE email = '{}') )""".format(name_param, value, email)
    connect_db(query)


def update_param_table_registration_data_db(email, name_param, value):
    query = """UPDATE registration_data SET {} = '{}' 
            WHERE email = '{}'""".format(name_param, value, email)
    connect_db(query)


def update_param_table_media_data_db(email, name_param, value):
    query = """UPDATE media_data SET {} = '{}'
    WHERE user_id =  (SELECT user_id FROM registration_data WHERE email = '{}') """.format(name_param, value, email)
    connect_db(query)


def update_param_table_contact_details_db(email, name_param, value):
    query = """UPDATE contact_details SET {} = '{}' WHERE user_id = ( SELECT user_id FROM registration_data 
    WHERE email = '{}')  """.format(name_param, value, email)
    connect_db(query)


def update_param_table_users_db(email, name_param, value):
    query = """UPDATE users SET {} = '{}' WHERE user_id = ( SELECT user_id FROM registration_data 
    WHERE email = '{}')""".format(
        name_param, value, email)
    connect_db(query)
