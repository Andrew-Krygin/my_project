# Список популярных платежных систем, карты которых обычно имеют 16 цифр в номере.
from datetime import datetime

from src.masks import LENGTH_ACCOUNT_NUM, LENGTH_CARD_NUM, data_validation, get_mask_account, get_mask_card_number

payment_systems = (
    "Visa", "Visa Classic", "Visa Gold", "Visa Platinum", "Visa Debit",
    "Mastercard", "MasterCard Standard", "MasterCard Gold", "MasterCard Platinum", "MasterCard Debit",
    "Maestro", "Maestro Debit", "Maestro Business", "Maestro Electronic",
)


def mask_account_card(payment_identifier: str) -> str:
    """Функция принимает один аргумент — строку, содержащую тип и номер карты или счета.
    И возвращает строку с замаскированным номером."""
    parts_pay_id = payment_identifier.split()

    if len(parts_pay_id) < 2:
        raise ValueError("""Недостаточно данных: должен быть тип и номер карты/счета.
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""")

    identifier = " ".join(parts_pay_id[: -1])
    numbers = parts_pay_id[-1]

    if identifier in payment_systems:
        correct_number = data_validation(numbers, LENGTH_CARD_NUM)
        masked = get_mask_card_number(correct_number)
    elif identifier == "Счет":
        correct_number = data_validation(numbers, LENGTH_ACCOUNT_NUM)
        masked = get_mask_account(correct_number)
    else:
        raise ValueError("""Неправильно указан тип карты или счета.
        Возможные варианты карт: Visa, Maestro, Mastercard
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""")
    return f"{identifier} {masked}"


def validate_date(date_and_time: str) -> bool:
    """Функция проверяет на валидность входящие данные на соответствие формату ISO 8601."""
    try:
        datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%S.%f')
        return True
    except ValueError:
        return False


def get_date(date_and_time: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"("11.03.2024")."""
    if validate_date(date_and_time):
        dt = datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%S.%f')
        date = datetime.strftime(dt, '%d.%m.%Y')
        return date
    raise TypeError("Неверный формат данных! Нужен формат ISO 8601.")
