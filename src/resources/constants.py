HOST = "127.0.0.1"
DB = "postgres"
USER = "postgres"
PASSWORD = 62823387
PORT = 5432

parameters = {
    'city': ['location', 'city'],
    'state': ['location', 'state'],
    'country': ['location', 'country'],
    'phone': ['phone'],
    'cell': ['cell'],
    'street_name': ['location', 'street', 'name'],
    'street_number': ['location', 'street', 'number'],
    'postcode': ['location', 'postcode'],
    'latitude': ['location', 'coordinates', 'latitude'],
    'longitude': ['location', 'coordinates', 'longitude'],
    'picture': ['picture', 'large'],
    'email': ['email'],
    'username': ['login', 'username'],
    'password': ['login', 'password'],
    'password_md5': ['login', 'md5'],
    'gender': ['gender'],
    'name_title': ['name', 'title'],
    'name_first': ['name', 'first'],
    'name_last': ['name', 'last'],
    'age': ['dob', 'age'],
    'nat': ['nat']
}

update_attr = {
    'city': ['cities'],
    'state': ['cities'],
    'country': ['cities'],
    'phone': ['contact_details'],
    'cell': ['contact_details'],
    'street_name': ['locations'],
    'street_number': ['locations'],
    'postcode': ['locations'],
    'latitude': ['locations'],
    'longitude': ['locations'],
    'picture': ['media_data'],
    'email': ['registration_data'],
    'username': ['registration_data'],
    'password': ['registration_data'],
    'password_md5': ['registration_data'],
    'gender': ['users'],
    'name_title': ['users'],
    'name_first': ['users'],
    'name_last': ['users'],
    'age': ['users'],
    'nat': ['users']
}