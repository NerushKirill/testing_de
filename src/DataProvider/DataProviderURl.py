import requests

from src.resources.constants import parameters


def get_user_url(num_user, url) -> dict:
    try:
        with requests.get(url + str(num_user)) as response:
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return {""}
    except requests.exceptions.MissingSchema:
        print("Ошибка: отсутствует схема в URL.")
        return {}
    except requests.exceptions.InvalidURL:
        print("Ошибка: некорректный URL.")
        return {}
    except requests.exceptions.ConnectionError:
        print("Ошибка: ошибка соединения.")
        return {}
    except requests.exceptions.Timeout:
        print("Ошибка: превышен лимит времени ожидания.")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Неизвестная ошибка: {e}")
        return {}


def parsing_json_file(data):
    dict_data: dict = {}
    for key, path in parameters.items():
        get_value = lambda results, path=path: eval("results" + "".join(f"['{x}']" for x in path))
        value = get_value(data['results'][0])
        dict_data[key] = value
    return dict_data

    # return email[0], password[0]
