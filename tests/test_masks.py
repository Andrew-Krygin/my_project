from contextlib import nullcontext as does_not_raise
from typing import ContextManager
from unittest.mock import patch

import pytest

from src.masks import (LENGTH_ACCOUNT_NUM, LENGTH_CARD_NUM, data_validation, get_mask_account, get_mask_card_number,
                       is_valid_number, request_valid_data)
from tests.fixtures.mask_cases import (ERROR_CASES_MASK_CARD_ACCOUNT, ERROR_CASES_NUMS, POSITIVE_CASES_MASK_ACCOUNT,
                                       POSITIVE_CASES_MASK_CARD, VALID_CASES_NUMS)


class TestValidNumbers:
    @pytest.mark.parametrize("args, res, expectation", VALID_CASES_NUMS)
    def test_positive_is_valid_number(self, args: tuple, res: bool, expectation: ContextManager) -> None:
        with expectation:
            assert is_valid_number(*args) == res

    @pytest.mark.parametrize("args, res, expectation", ERROR_CASES_NUMS)
    def test_negative_is_valid_number(self, args: tuple, res: bool, expectation: ContextManager) -> None:
        with expectation:
            assert is_valid_number(*args) == res

    @pytest.mark.parametrize(
        "input_data, expected, length, expectation",
        [
            # Тест валидации для карты
            (
                ["123", "asd12345678", "dfgrtwsd", "", "1234567890987654"],
                "1234567890987654",
                LENGTH_CARD_NUM,
                does_not_raise(),
            ),
            # Тест валидации аккаунта
            (
                ["593", "ajyufd45678", "dfgrtwsd", "", "12345678909876543212"],
                "12345678909876543212",
                LENGTH_ACCOUNT_NUM,
                does_not_raise(),
            ),
        ],
    )
    def test_request_valid_data(
        self, input_data: list, expected: str, length: int, expectation: ContextManager
    ) -> None:
        with patch("builtins.input", side_effect=input_data):
            with expectation:
                result = request_valid_data("1232323asas", length)
                assert result == expected

    @pytest.mark.parametrize(
        "input_value, side_effect_input, length, expected, expectation",
        [  # Тесты для карт
            ("1234567898765432", [], LENGTH_CARD_NUM, "1234567898765432", does_not_raise()),
            (
                "123asd",
                ["asjcanf1223", "1234", "1234567898765432"],
                LENGTH_CARD_NUM,
                "1234567898765432",
                does_not_raise(),
            ),
            # Тесты для аккаунта
            ("12345678987654321234", [], LENGTH_ACCOUNT_NUM, "12345678987654321234", does_not_raise()),
            (
                "12asde",
                ["1asjcanf1223", "1234", "12345678987654321234"],
                LENGTH_ACCOUNT_NUM,
                "12345678987654321234",
                does_not_raise(),
            ),
        ],
    )
    def test_data_validation(
        self, input_value: str, side_effect_input: list, length: int, expected: str, expectation: ContextManager
    ) -> None:
        with patch("builtins.input", side_effect=side_effect_input):
            with expectation:
                result = data_validation(input_value, length)
                assert result == expected


class TestMaskCardAccount:
    @pytest.mark.parametrize("input_data, res, expectation", POSITIVE_CASES_MASK_CARD)
    def test_valid_get_mask_card_number(self, input_data: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = get_mask_card_number(input_data)
            assert result == res

    @pytest.mark.parametrize("input_data, res, expectation", ERROR_CASES_MASK_CARD_ACCOUNT)
    def test_invalid_get_mask_card_number(self, input_data: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = get_mask_card_number(input_data)
            assert result == res

    @pytest.mark.parametrize("input_data, res, expectation", POSITIVE_CASES_MASK_ACCOUNT)
    def test_valid_get_mask_account(self, input_data: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = get_mask_account(input_data)
            assert result == res

    @pytest.mark.parametrize("input_data, res, expectation", ERROR_CASES_MASK_CARD_ACCOUNT)
    def test_invalid_get_mask_account(self, input_data: str, res: str, expectation: ContextManager) -> None:
        with expectation:
            result = get_mask_account(input_data)
            assert result == res
