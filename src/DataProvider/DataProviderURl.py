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
    except requests.exceptions.MissingSchema as me:
        print(f"Ошибка: отсутствует схема в URL. {me}")
        return {}
    except requests.exceptions.InvalidURL as ie:
        print(f"Ошибка: некорректный URL. {ie}")
        return {}
    except requests.exceptions.ConnectionError as ce:
        print(f"Ошибка: ошибка соединения. {ce}")
        return {}
    except requests.exceptions.Timeout as te:
        print(f"Ошибка: превышен лимит времени ожидания. {te}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: ошибка запроса. {e}")
        return {}


def parsing_json_file(data):
    dict_data: dict = {}
    for key, path in parameters.items():
        get_value = lambda results, path=path: eval("results" + "".join(f"['{x}']" for x in path))
        value = get_value(data['results'][0])
        dict_data[key] = value
    return dict_data

