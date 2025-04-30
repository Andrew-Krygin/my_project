import pytest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from src.widget import mask_account_card

ERROR_MESSAGE_1 = """Недостаточно данных: должен быть тип и номер карты/счета.
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560"""

ERROR_MESSAGE_2 = """Неправильно указан тип карты или счета.
        Возможные варианты карт: Visa, Maestro, Mastercard
        Пример: Visa Classic 6831982476737658
                Счет 35383033474447895560"""


@pytest.mark.parametrize(
    "card, res, expectation",
    [   # Тесты для карты
        ("Visa 1212345678908978", "Visa 1212 34** **** 8978", does_not_raise()),
        ("Visa Classic 1212345678908978", "Visa Classic 1212 34** **** 8978", does_not_raise()),
        ("Mastercard 0987654321234567", "Mastercard 0987 65** **** 4567", does_not_raise()),
        ("Maestro Business 0000000000000000", "Maestro Business 0000 00** **** 0000", does_not_raise()),
        ("                   ", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("Visa Glass 1212345678908978", "", pytest.raises(ValueError, match=ERROR_MESSAGE_2)),
        ("Maestric 0987654321122334", "", pytest.raises(ValueError, match=ERROR_MESSAGE_2)),
        ("Mastercard1234567890876543", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("1232345676545678", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("><.,'; 1234567876543212,", "", pytest.raises(ValueError, match=ERROR_MESSAGE_2)),
        ("", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),

        # Тесты для счета
        ("Счет 23456789098765432123", "Счет **2123", does_not_raise()),
        ("Счет 00000000000000000000", "Счет **0000", does_not_raise()),
        ("                             ", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("Счет12233445566778899098", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("Счит 34243434343434343434", "", pytest.raises(ValueError, match=ERROR_MESSAGE_2)),
        ("121234455665544345567665", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
        ("", "", pytest.raises(ValueError, match=ERROR_MESSAGE_1)),
    ]
)
def test_mask_account_card(card: str, res: str, expectation) -> None:
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
def test_mask_account_card_retry(input_data: str, side_effect_input: list, res: str, expectation) -> None:
    with patch("builtins.input", side_effect=side_effect_input):
        with expectation:
            result = mask_account_card(input_data)
            assert result == res
