from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PATH_TO_FILE_CSV = DATA_DIR / "transactions.csv"
PATH_TO_FILE_XLSX = DATA_DIR / "transactions_excel.xlsx"


def transaction_read_csv(path_to_file_csv: Path) -> list[dict]:
    """
    Функция считывает финансовые операции из CSV и выдает список словарей с транзакциями.
    :param path_to_file_csv: Путь к файлу transactions.csv.
    :return: Список словарей с транзакциями.
    """
    if not isinstance(path_to_file_csv, Path):
        raise ValueError("Путь к файлу должен иметь Path - тип.")

    try:
        transactions = pd.read_csv(path_to_file_csv, sep=";")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл по пути {path_to_file_csv} не найден.")

    list_transactions = transactions.to_dict(orient="records")

    return list_transactions


def transaction_read_xlsx(path_to_file_xlsx: Path) -> list:
    """
    Функция считывает финансовые операции из Excel и выдает список словарей с транзакциями.
    :param path_to_file_xlsx: Путь к файлу transactions.csv.
    :return: Список словарей с транзакциями.
    """
    if not isinstance(path_to_file_xlsx, Path):
        raise ValueError("Путь к файлу должен иметь Path - тип.")

    try:
        transactions = pd.read_excel(path_to_file_xlsx)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл по пути {path_to_file_xlsx} не найден.")

    list_transactions = transactions.to_dict(orient="records")

    return list_transactions
