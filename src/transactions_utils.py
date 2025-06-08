from src.generators import filter_by_currency
from src.processing import search_transactions_by_query, sort_by_date
from src.transaction_read import PATH_TO_FILE_CSV, PATH_TO_FILE_XLSX, transaction_read_csv, transaction_read_xlsx
from src.utils import PATH_TO_FILE, load_transactions
from src.widget import get_date, mask_account_card

# Пункты меню.
MENU_ITEMS = {
    1: "Для обработки выбран JSON-файл.",
    2: "Для обработки выбран CSV-файл.",
    3: "Для обработки выбран XLSX-файл.",
}

# Загружает файл в зависимости от выбора пользователя.
LOAD_FILE = {
    1: lambda: load_transactions(PATH_TO_FILE),
    2: lambda: transaction_read_csv(PATH_TO_FILE_CSV),
    3: lambda: transaction_read_xlsx(PATH_TO_FILE_XLSX),
}

# Статусы для фильтрации списка транзакций.
TRANSACTION_STATUS = ["EXECUTED", "CANCELED", "PENDING"]


def show_menu() -> None:
    """
    Функция выводит на экран меню программы.
    :return: None
    """
    print(
        """
Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
"""
    )


def validate_choice() -> int:
    """
    Функция запрашивает у пользователя выбор пункта меню (1–3) и обрабатывает возможные ошибки ввода.
    :return: Корректный выбор пользователя (целое число от 1 до 3)
    """
    while True:
        try:
            choice = int(input("Пользователь: "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Ошибка: Введите число от 1 до 3.")
        except ValueError:
            print("Ошибка: Введите число от 1 до 3.")


def validate_transact_status() -> str:
    """
    Функция предлагает пользователю выбрать статус фильтрации и обрабатывает ответ пока он не будет корректным.
    :return: Корректный выбор пользователя (статусы: EXECUTED, CANCELED, PENDING)
    """
    while True:
        status = (
            input(
                "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: "
            )
            .strip()
            .upper()
        )
        if status in TRANSACTION_STATUS:
            return status
        else:
            print(f"Статус операции '{status}' недоступен.")


def ask_sort_by_date(list_transactions: list[dict]) -> list[dict]:
    """
    Функция сортирует список транзакций по дате(убывание/возрастание) или оставляет все как есть по выбору
    пользователя.
    :param list_transactions: Список транзакций.
    :return: Список транзакций.
    """
    sort_date = input("Отсортировать по дате? Да/Нет: ").strip().lower()

    if sort_date == "да":
        descending = input("Отсортировать по возрастанию или по убыванию?: ").strip().lower()
        if descending == "по возрастанию":
            return sort_by_date(list_transactions, False)
        return sort_by_date(list_transactions)
    return list_transactions


def ask_filter_by_currency(list_transactions: list[dict]) -> list[dict]:
    """
    Функция фильтрует список транзакций по валюте или оставляет все как есть по выбору пользователя.
    :param list_transactions: Список транзакций.
    :return: Список транзакций.
    """
    rub_transact = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()

    if rub_transact == "да":
        return list(filter_by_currency(list_transactions, "RUB"))
    return list_transactions


def ask_filter_by_query(list_transactions: list[dict]) -> list[dict]:
    """
    Функция фильтрует список транзакций по определенному слову или оставляет все как есть по выбору пользователя.
    :param list_transactions: Список транзакций.
    :return: Список транзакций.
    """
    filter_transact_by_query = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    )

    # Оставляем транзакции которые включают в себя слово для поиска если пользователь согласился.
    if filter_transact_by_query == "да":
        query = input("Введите слово для поиска: ").strip()
        return search_transactions_by_query(list_transactions, query)
    return list_transactions


def apply_user_filters(list_transactions: list[dict]) -> list[dict]:
    """
    Запрашивает у пользователя параметры фильтрации и сортировки и применяет их к списку транзакций.
    :param list_transactions: Список транзакций.
    :return: Список транзакций.
    """
    transactions = ask_sort_by_date(list_transactions)
    transactions = ask_filter_by_currency(transactions)
    transactions = ask_filter_by_query(transactions)
    return transactions


def show_opening_a_deposit(transaction: dict) -> None:
    """
    Функция выводит на экран информацию о банковской операции "Открытие вклада"
    :param transaction: Словарь с данными одной банковской транзакции.
    :return: None
    """
    # Промежуточные переменные чтобы mypy не выдавал ошибки.
    description: str = transaction.get("description", "")
    date_str: str = transaction.get("date", "")
    to_account: str = transaction.get("to", "")

    date = get_date(date_str)
    account = mask_account_card(to_account)
    if "operationAmount" in transaction:
        amount = transaction.get("operationAmount", {}).get("amount")
        currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
    else:
        amount = transaction.get("amount")
        currency_name = transaction.get("currency_name")

    print(f"{date} {description}\n" f"{account}\n" f"Сумма: {amount} {currency_name}")


def show_transfer(transaction: dict) -> None:
    """
    Выводит на экран информацию о переводах.
    :param transaction: Словарь с данными одной банковской транзакции.
    :return: None
    """
    # Промежуточные переменные чтобы mypy не выдавал ошибки.
    description: str = transaction.get("description", "")
    date_str: str = transaction.get("date", "")
    from_account: str = transaction.get("from", "")
    to_account: str = transaction.get("to", "")

    date = get_date(date_str)
    from_transfer = mask_account_card(from_account)
    to_transfer = mask_account_card(to_account)

    if "operationAmount" in transaction:
        amount = transaction.get("operationAmount", {}).get("amount")
        currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
    else:
        amount = transaction.get("amount")
        currency_name = transaction.get("currency_name")

    print(f"{date} {description}\n" f"{from_transfer} -> {to_transfer}\n" f"Сумма: {amount} {currency_name}")


def print_transactions(list_transactions: list[dict]) -> None:
    """
    Выводит на экран список транзакций, отформатированных по типу операции.

    - Если список пуст, информирует пользователя об отсутствии подходящих транзакций.
    - Если транзакция содержит описание "Открытие вклада", используется формат вывода для вкладов.
    - В остальных случаях используется формат вывода для переводов.
    :param list_transactions: Список словарей, где каждый словарь содержит данные одной банковской операции.
    :return: None
    """
    if not list_transactions:
        print()
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(list_transactions)}")
    print()
    for trans in list_transactions:
        if trans.get("description", "").lower() == "открытие вклада":
            show_opening_a_deposit(trans)
        else:
            show_transfer(trans)
        print()
