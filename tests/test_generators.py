import re
from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from tests.fixtures.error_messages import ERROR_MESSAGE_GENERATORS
from tests.fixtures.transactions import RUB_TRANSACTIONS, USD_TRANSACTIONS


class TestFilterByCurrency:
    @pytest.mark.parametrize(
        "currency, res",
        [
            ("RUB", RUB_TRANSACTIONS),
            ("USD", USD_TRANSACTIONS),
        ],
    )
    def test_filter_by_currency(self, sample_transactions: list[dict], currency: str, res: list[dict]) -> None:
        with does_not_raise():
            result = list(filter_by_currency(sample_transactions, currency))
            assert result == res

    @pytest.mark.parametrize(
        "test_case, currency, res",
        [
            (RUB_TRANSACTIONS + USD_TRANSACTIONS, "EUR", []),
            ([{}, {}, {}], "USD", []),
        ],
    )
    def test_invalid_filter_by_currency(self, test_case: list[dict], currency: str, res: list) -> None:
        with does_not_raise():
            result = list(filter_by_currency(test_case, currency))
            assert result == res

    @pytest.mark.parametrize(
        "invalid_input, res",
        [
            (
                [
                    {},
                    {"operationAmount": {}},
                    {"operationAmount": {"currency": {}}},
                    {"operationAmount": {"currency": {"code": None}}},
                ],
                [],
            ),
        ],
    )
    def test_filter_by_currency_with_incomplete_data(self, invalid_input: list[dict], res: list) -> None:
        with does_not_raise():
            result = list(filter_by_currency(invalid_input, "USD"))
            assert result == res


class TestTransactionDescriptions:
    @pytest.mark.parametrize(
        "res",
        [
            (
                [
                    "Перевод организации",
                    "Перевод со счета на счет",
                    "Перевод со счета на счет",
                    "Перевод со счета на счет",
                ]
            ),
        ],
    )
    def test_transaction_descriptions(self, sample_transactions: list[dict], res: list) -> None:
        with does_not_raise():
            result = transaction_descriptions(sample_transactions)
            assert list(result) == res

    @pytest.mark.parametrize(
        "test_case, res",
        [
            (USD_TRANSACTIONS, ["Перевод организации", "Перевод со счета на счет"]),
            ([{}, {}, {}], []),
        ],
    )
    def test_transaction_descriptions_various_cases(self, test_case: list[dict], res: list) -> None:
        with does_not_raise():
            result = list(transaction_descriptions(test_case))
            assert result == res


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "test_case, res, expectation",
        [
            ((1, 2), ["0000 0000 0000 0001", "0000 0000 0000 0002"], does_not_raise()),
            (
                (10, 13),
                ["0000 0000 0000 0010", "0000 0000 0000 0011", "0000 0000 0000 0012", "0000 0000 0000 0013"],
                does_not_raise(),
            ),
            ((0, 4), None, pytest.raises(ValueError, match=re.escape(ERROR_MESSAGE_GENERATORS["invalid_start"]))),
            (
                (11111111111111111, 99999999999999999),
                None,
                pytest.raises(ValueError, match=re.escape(ERROR_MESSAGE_GENERATORS["invalid_len"])),
            ),
        ],
    )
    def test_card_number_generator(
        self, test_case: tuple[int, int], res: list[dict], expectation: ContextManager
    ) -> None:
        with expectation:
            result = list(card_number_generator(*test_case))
            assert result == res

    @pytest.mark.parametrize(
        "start, stop",
        [
            (1, 5),
            (100, 105),
            (999, 1003),
        ],
    )
    def test_card_number_generator_various_ranges(self, start: int, stop: int) -> None:
        cards = list(card_number_generator(start, stop))
        assert len(cards) == (stop - start + 1)

    def test_card_number_generator_format(self) -> None:
        start = 123
        stop = 125
        cards = list(card_number_generator(start, stop))

        for card in cards:
            assert len(card) == 19
            assert card[4] == " "
            assert card[9] == " "
            assert card[14] == " "
