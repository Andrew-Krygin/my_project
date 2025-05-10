import pytest
from contextlib import nullcontext as does_not_raise
from src.masks import LENGTH_ACCOUNT_NUM, LENGTH_CARD_NUM


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
