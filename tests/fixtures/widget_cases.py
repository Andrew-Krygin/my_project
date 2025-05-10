from contextlib import nullcontext as does_not_raise

import pytest

from tests.fixtures.error_messages import ERROR_MESSAGES_WIDGET

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
    ("                   ", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("Visa Glass 1212345678908978", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["incorrect_type"])),
    ("Maestric 0987654321122334", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["incorrect_type"])),
    ("Mastercard1234567890876543", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("1232345676545678", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("><.,'; 1234567876543212,", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["incorrect_type"])),
    ("", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    # Тесты для счета
    ("                             ", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("Счет12233445566778899098", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("Счит 34243434343434343434", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["incorrect_type"])),
    ("121234455665544345567665", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
    ("", "", pytest.raises(ValueError, match=ERROR_MESSAGES_WIDGET["missing_data"])),
]
