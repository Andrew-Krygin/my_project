import re
from collections import Counter


def filter_by_state(records: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция принимает список словарей и опционально значение для ключа state(по умолчанию 'EXECUTED').
    И возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    selected_records = [record for record in records if record.get("state") == state]
    return selected_records


def sort_by_date(records: list[dict], decreasing: bool = True) -> list[dict]:
    """
    Функция принимает список словарей и необязательный параметр, задающий порядок
    сортировки (по умолчанию — убывание). А затем возвращает новый список, отсортированный по дате (date).
    """
    sorted_records_of_date = sorted(records, key=lambda record: record.get("date", ""), reverse=decreasing)
    return sorted_records_of_date


def search_transactions_by_query(transactions: list[dict], query: str) -> list[dict]:
    """
    Функцию принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка.
    :param transactions: Список транзакций. Тип данных: list[dict].
    :param query: Строка по которой осуществляется поиск транзакций.
    :return: Список словарей, у которых в описании есть данная строка.
    """
    if not isinstance(transactions, list):
        raise ValueError(f"Expected a list, but got {type(transactions)}")
    if not isinstance(query, str):
        raise ValueError(f"Expected a string for query, but got {type(query)}")

    return [
        transact
        for transact in transactions
        if isinstance(transact, dict) and re.search(query, transact.get("description", ""), re.IGNORECASE)
    ]


def count_operations_by_category(transactions: list[dict], categories: list) -> dict[str, int]:
    """
    :param transactions: Список словарей с данными о банковских операциях.
    :param categories: Список категорий операций.
    :return: Словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой
    категории.
    """
    if not isinstance(transactions, list):
        raise ValueError(f"Expected a list, but got {type(transactions)}")

    if not isinstance(categories, list):
        raise ValueError(f"Expected a list, but got {type(categories)}")

    matched_categories = []

    for transact in transactions:
        if isinstance(transact, dict):
            category = transact.get("description", "")
            if category in categories:
                matched_categories.append(category)

    counted = Counter(matched_categories)

    return counted
