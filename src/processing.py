def filter_by_state(records: list[dict[str, int | str]], state: str = "EXECUTED") -> list[dict[str, int | str]]:
    """
    Функция принимает список словарей и опционально значение для ключа state(по умолчанию 'EXECUTED').
    И возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    selected_records = [record for record in records if record.get("state") == state]
    return selected_records
