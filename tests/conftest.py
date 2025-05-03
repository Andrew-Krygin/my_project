from contextlib import nullcontext as does_not_raise

import pytest

from src.masks import LENGTH_ACCOUNT_NUM, LENGTH_CARD_NUM


@pytest.fixture
def sample_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 41428829, "state": "EXECUTED"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 615414851, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]


@pytest.fixture
def empty_data():
    return [
        {},
        {},
        {},
    ]


@pytest.fixture
def invalid_type_data():
    return [1234, ("aededa",), set()]


@pytest.fixture
def invalid_date_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": None},
        {"id": 41428829, "state": "EXECUTED", "date": 1234},
        {"id": 41428829, "state": "CANCELED", "date": "не_дата"},
        {"id": 41428829, "state": "CANCELED"},
    ]


# Сообщения об ошибки для модуля test_widget.
ERROR_MESSAGES = {
    "missing_data": """Недостаточно данных: должен быть тип и номер карты/счета.
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""",
    "incorrect_type": """Неправильно указан тип карты или счета.
        Возможные варианты карт: Visa, Maestro, Mastercard
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""",
    "invalid_date_format": "Неверный формат данных! Нужен формат ISO 8601.",
}

# Позитивные кейсы для функции test_mask_account_card из класса TestMasks модуля test_widget.
VALID_CASES_MASKS = [
    # Тесты для карты
    ("Visa 1212345678908978", "Visa 1212 34** **** 8978", does_not_raise()),
    ("Visa Classic 1212345678908978", "Visa Classic 1212 34** **** 8978", does_not_raise()),
    ("Mastercard 0987654321234567", "Mastercard 0987 65** **** 4567", does_not_raise()),
    ("Maestro Business 0000000000000000", "Maestro Business 0000 00** **** 0000", does_not_raise()),
    # Тесты для счета
    ("Счет 23456789098765432123", "Счет **2123", does_not_raise()),
    ("Счет 00000000000000000000", "Счет **0000", does_not_raise()),
]

# Негативные кейсы для функции test_mask_account_card из класса TestMasks модуля test_widget.
ERROR_CASES_MASKS = [
    # Тесты для карты
    ("                   ", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("Visa Glass 1212345678908978", "", pytest.raises(ValueError, match=ERROR_MESSAGES["incorrect_type"])),
    ("Maestric 0987654321122334", "", pytest.raises(ValueError, match=ERROR_MESSAGES["incorrect_type"])),
    ("Mastercard1234567890876543", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("1232345676545678", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("><.,'; 1234567876543212,", "", pytest.raises(ValueError, match=ERROR_MESSAGES["incorrect_type"])),
    ("", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    # Тесты для счета
    ("                             ", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("Счет12233445566778899098", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("Счит 34243434343434343434", "", pytest.raises(ValueError, match=ERROR_MESSAGES["incorrect_type"])),
    ("121234455665544345567665", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
    ("", "", pytest.raises(ValueError, match=ERROR_MESSAGES["missing_data"])),
]

# Позитивные кейсы для функции test_is_valid_number из класса TestValidNumbers модуля test_masks.
VALID_CASES_NUMS = [
    # Тесты для карт
    (("1234567898765432", LENGTH_CARD_NUM), True, does_not_raise()),
    (("0000000000000000", LENGTH_CARD_NUM), True, does_not_raise()),
    (("qwsa@er'gt,uhj.n", LENGTH_CARD_NUM), False, does_not_raise()),
    (("123bc", LENGTH_CARD_NUM), False, does_not_raise()),
    (("", LENGTH_CARD_NUM), False, does_not_raise()),
    # Тесты для аккаунта
    (("12345678987654321234", LENGTH_ACCOUNT_NUM), True, does_not_raise()),
    (("00000000000000000000", LENGTH_ACCOUNT_NUM), True, does_not_raise()),
    (("qwertfgh;y'u,j.kiolm", LENGTH_ACCOUNT_NUM), False, does_not_raise()),
    (("123bc", LENGTH_ACCOUNT_NUM), False, does_not_raise()),
    (("", LENGTH_ACCOUNT_NUM), False, does_not_raise()),
]

# Негативные кейсы для функции test_is_valid_number из класса TestValidNumbers модуля test_masks.
ERROR_CASES_NUMS = [
    # Тесты для карт
    ((1234567876543212, LENGTH_CARD_NUM), None, pytest.raises(AttributeError)),
    (("1234567898765432",), None, pytest.raises(TypeError)),
    # Тесты для аккаунта
    ((12345678765432120909, LENGTH_ACCOUNT_NUM), None, pytest.raises(AttributeError)),
    (("12345678987654329876",), None, pytest.raises(TypeError)),
]

# Негативные кейсы для функций: test_get_mask_card_number, test_get_mask_account
# из класса TestMaskCardAccount модуля test_masks.
ERROR_CASES_MASK_CARD_ACCOUNT = [
    # Тесты для карт и аккаунта
    (None, None, pytest.raises(TypeError)),
    (1234, None, pytest.raises(TypeError)),
]
