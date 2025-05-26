import json
import os

BASE_DIR = os.path.dirname(__file__)
PATH_TO_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "operations.json")


def load_transactions(path_to_file: str) -> list:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными
    о финансовых транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    if not isinstance(path_to_file, str):
        raise TypeError

    try:
        with open(path_to_file, encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list) and data:
                return data
            else:
                return []
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")

    return []
