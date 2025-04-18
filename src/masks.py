# Константы, указывают количество цифр в номере карты и в аккаунте.
LENGTH_CARD_NUM = 16
LENGTH_ACCOUNT_NUM = 20


def data_validation(input_nums: str, length: int) -> str:
    """Функция осуществляет валидацию входных данных. Это либо номер карты, либо номер счета.
    Если введенные данные не соответствуют критериям валидации, функция просит ввести корректные
    данные. Если данные соответствуют критериям, возвращает результат.
    """
    while len(input_nums) != length or not input_nums.isdigit():
        print("Ошибка! Введите корректные данные!\n" f"Номер содержит {length} цифр: ", end="")
        input_nums = input()
        print()
    return input_nums


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску.
    Номер карты замаскирован и отображается в формате XXXX XX** **** XXXX
    """
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX
    """
    return f"**{account_number[-4:]}"
