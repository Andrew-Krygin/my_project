def filter_by_state(records: list[dict[str, int | str]], state: str = "EXECUTED") -> list[dict[str, int | str]]:
    """
    Функция принимает список словарей и опционально значение для ключа state(по умолчанию 'EXECUTED').
    И возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    selected_records = [record for record in records if record.get("state") == state]
    return selected_records


def sort_by_date(records: list[dict[str, int | str]], decreasing: bool = True) -> list[dict[str, int | str]]:
    """
    Функция принимает список словарей и необязательный параметр, задающий порядок
    сортировки (по умолчанию — убывание). А затем возвращает новый список, отсортированный по дате (date).
    """
    sorted_records_of_date = sorted(records, key=lambda record: record.get("date", ""), reverse=decreasing)
    return sorted_records_of_date
