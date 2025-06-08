from contextlib import nullcontext as does_not_raise
from typing import ContextManager
from unittest.mock import patch

import pytest

from src.widget import get_date, mask_account_card
from tests.fixtures.error_messages import ERROR_MESSAGES_WIDGET
from tests.fixtures.widget_cases import ERROR_CASES_MASKS, VALID_CASES_MASKS


class TestMasks:
    @pytest.mark.parametrize("card, res, expectation", VALID_CASES_MASKS)
    def test_valid_mask_account_card(self, card: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = mask_account_card(card)
            assert result == res

    @pytest.mark.parametrize("card, res, expectation", ERROR_CASES_MASKS)
    def test_invalid_mask_account_card(self, card: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = mask_account_card(card)
            assert result == res

    @pytest.mark.parametrize(
        "input_data, side_effect_input, res, expectation",
        [  # Тест для карт
            ("Visa 435432", [" ", "234234234", "1223345678909876"], "Visa 1223 34** **** 9876", does_not_raise()),
            ("Visa 12#34@56,8.0!978", ["", "4343545465768776"], "Visa 4343 54** **** 8776", does_not_raise()),
            # Тест для счета
            ("Счет 1234", [" ", "45673756756474563", "00000000000000000000"], "Счет **0000", does_not_raise()),
            ("Счет 12@2,44.5!76#567№909", ["", "12233445566778890998"], "Счет **0998", does_not_raise()),
        ],
    )
    def test_mask_account_card_retry(
        self, input_data: str, side_effect_input: list, res: str, expectation: ContextManager
    ) -> None:
        with patch("builtins.input", side_effect=side_effect_input):
            with expectation:
                result = mask_account_card(input_data)
                assert result == res


class TestDate:
    @pytest.mark.parametrize(
        "data, res, expectation",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024", does_not_raise()),
            ("2024-03-11", "11.03.2024", does_not_raise()),
            ("11.03.2024", "11.03.2024", does_not_raise()),
            ("March 11, 2024", "11.03.2024", does_not_raise()),
            ("11 Mar 2024", "11.03.2024", does_not_raise()),
            ("вчера", None, pytest.raises(TypeError, match=ERROR_MESSAGES_WIDGET["invalid_date_format"])),
            ("", None, pytest.raises(TypeError, match=ERROR_MESSAGES_WIDGET["invalid_date_format"])),
            ("           ", None, pytest.raises(TypeError, match=ERROR_MESSAGES_WIDGET["invalid_date_format"])),
            (12032024, None, pytest.raises(TypeError)),
        ],
    )
    def test_get_date(self, data: str, res: bool, expectation: ContextManager) -> None:
        with expectation:
            result = get_date(data)
            assert result == res
