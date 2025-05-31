import json
import os

from src.general_logger_settings import setup_logger

BASE_DIR = os.path.dirname(__file__)
PATH_TO_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "operations.json")


utils_logger = setup_logger(__name__, log_file="utils.log")


def load_transactions(path_to_file: str) -> list:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными
    о финансовых транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    utils_logger.info("Функция начинает свое выполнение.")
    if not isinstance(path_to_file, str):
        utils_logger.exception("Файл поврежден или отсутствует.")
        raise TypeError

    try:
        utils_logger.info("Открываем файл %s", path_to_file)
        with open(path_to_file, encoding="utf-8") as file:
            utils_logger.info("Считываем данные.")
            data = json.load(file)
            if isinstance(data, list) and data:
                utils_logger.info("Тип данных корректен, файл не пустой. Возвращаем данные.")
                return data
            else:
                utils_logger.warning(
                    "Тип данных не корректен или файл пустой. Возвращается значение по умолчанию: 0.0."
                )
                return []
    except FileNotFoundError as e:
        utils_logger.exception("Ошибка! | Тип: %s", type(e).__name__)
        print(f"Файл не найден: {e}")
    except json.JSONDecodeError as e:
        utils_logger.exception("Ошибка! | Тип: %s", type(e).__name__)
        print(f"Ошибка декодирования JSON: {e}")

    utils_logger.info("Возвращается значение по умолчанию: 0.0.")
    return []
