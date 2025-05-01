from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

import pytest

from src.widget import get_date, mask_account_card, validate_date

ERROR_MESSAGES = {
    "missing_data": """Недостаточно данных: должен быть тип и номер карты/счета.
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""",
    "incorrect_type": """Неправильно указан тип карты или счета.
        Возможные варианты карт: Visa, Maestro, Mastercard
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560""",
    "invalid_date_format": "Неверный формат данных! Нужен формат ISO 8601."
}

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


class TestMasks:
    @pytest.mark.parametrize("card, res, expectation", VALID_CASES_MASKS + ERROR_CASES_MASKS)
    def test_mask_account_card(self, card: str, res: str, expectation) -> None:
        with expectation:
            result = mask_account_card(card)
            assert result == res

    @pytest.mark.parametrize(
        "input_data, side_effect_input, res, expectation",
        [   # Тест для карт
            ("Visa 435432", [" ", "234234234", "1223345678909876"], "Visa 1223 34** **** 9876", does_not_raise()),
            ("Visa 12#34@56,8.0!978", ["", "4343545465768776"], "Visa 4343 54** **** 8776", does_not_raise()),

            # Тест для счета
            ("Счет 1234", [" ", "45673756756474563", "00000000000000000000"], "Счет **0000", does_not_raise()),
            ("Счет 12@2,44.5!76#567№909", ["", "12233445566778890998"], "Счет **0998", does_not_raise()),
        ]
    )
    def test_mask_account_card_retry(
            self, input_data: str, side_effect_input: list, res: str, expectation) -> None:
        with patch("builtins.input", side_effect=side_effect_input):
            with expectation:
                result = mask_account_card(input_data)
                assert result == res


class TestDate:
    @pytest.mark.parametrize(
        "data, res, expectation",
        [
            ("2024-03-11T02:26:18.671407", True, does_not_raise()),
            ("2024-03-11T02:26:18", False, does_not_raise()),
            ("11.03.2021", False, does_not_raise()),
            ("03/11/2022", False, does_not_raise()),
            ("2024/03/11", False, does_not_raise()),
            ("2024@03@11", False, does_not_raise()),
            ("", False, does_not_raise()),
            ("           ", False, does_not_raise()),
            (12032024, None, pytest.raises(TypeError)),
        ]
    )
    def test_validate_date(self, data, res, expectation):
        with expectation:
            result = validate_date(data)
            assert result == res

    @pytest.mark.parametrize(
        "data, res, expectation",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024", does_not_raise()),
            ("11.03.2021", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            ("03/11/2022", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            ("2024/03/11", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            ("2024@03@11", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            ("", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            ("           ", None, pytest.raises(TypeError, match=ERROR_MESSAGES["invalid_date_format"])),
            (12032024, None, pytest.raises(TypeError)),
        ]
    )
    def test_get_date(self, data, res, expectation):
        with expectation:
            result = get_date(data)
            assert result == res
