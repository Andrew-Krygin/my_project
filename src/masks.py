# Константы, указывают количество цифр в номере карты и в аккаунте.
LENGTH_CARD_NUM = 16
LENGTH_ACCOUNT_NUM = 20


def is_valid_number(input_value: str, length: int) -> bool:
    """Функция проверяет корректность вводимых данных."""
    return input_value.isdigit() and len(input_value) == length


def request_valid_data(input_value: str, length: int) -> str:
    """Функция запрашивает данные у пользователя до тех пор, пока они не станут валидными."""
    while not is_valid_number(input_value, length):
        print("Ошибка! Введите корректные данные!\n" f"Номер содержит {length} цифр: ", end="")
        input_value = input()
        print()
    return input_value


def data_validation(input_value: str, length: int) -> str:
    """Функция осуществляет валидацию входных данных. Это либо номер карты, либо номер счета.
    Если введенные данные не соответствуют критериям валидации, функция просит ввести корректные
    данные. Если данные соответствуют критериям, возвращает результат.
    """
    if is_valid_number(input_value, length):
        return input_value
    return request_valid_data(input_value, length)


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
