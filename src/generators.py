from typing import Iterator


def filter_by_currency(lst_transactions: list[dict], currency: str) -> Iterator[dict]:
    """Функция возвращает итератор, который поочередно выдает транзакции, где валюта
    операции соответствует заданной."""
    for transact in lst_transactions:
        currency_name = transact.get("operationAmount", {}).get("currency", {}).get("code")

        if currency_name == currency:
            yield transact


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    for transaction in transactions:
        description = transaction.get("description")

        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Функция генерирует номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."""
    if start < 1:
        raise ValueError("Номер карты должен начинаться с 1 или выше (0 — недопустим).")

    len_card = 16

    for num in range(start, stop + 1):
        str_digit = str(num)
        if len(str_digit) > len_card:
            raise ValueError(f"Значение не может быть больше {len_card} цифр.")

        str_card = str_digit.zfill(len_card)
        card = f"{str_card[:4]} {str_card[4:8]} {str_card[8:12]} {str_card[12:16]}"

        yield card
