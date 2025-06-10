from contextlib import nullcontext as does_not_raise
from typing import ContextManager
from unittest.mock import Mock, patch

import pytest

from src.transactions_utils import (apply_user_filters, ask_filter_by_currency, ask_filter_by_query, ask_sort_by_date,
                                    print_transactions, show_menu, show_opening_a_deposit, show_transfer,
                                    validate_choice, validate_transact_status)
from tests.fixtures.cases_for_transactions_utils import (ALL_CURRENCY_TRANSACTIONS, OPENING_DEPOSIT, PRINT_OUT,
                                                         RUB_CURRENCY_TRANSACTIONS, SAMPLE_TRANSACTIONS,
                                                         SORT_BY_DATE_ASCENDING, SORT_BY_DATE_DESCENDING,
                                                         SORT_BY_DATE_NO_SORT, TRANSACTIONS_FILTER_BY_QUERY_OPENING,
                                                         TRANSACTIONS_FILTER_BY_QUERY_TRANSFER,
                                                         TRANSACTIONS_FILTER_NO_QUERY, TRANSFER_TRANSACTIONS)


class TestTransactionsUtils:
    def test_show_menu(self, capsys: pytest.CaptureFixture) -> None:
        show_menu()
        captured = capsys.readouterr()
        assert captured.out == (
            "\nПривет! Добро пожаловать в программу работы с банковскими транзакциями."
            "\nВыберите необходимый пункт меню:"
            "\n1. Получить информацию о транзакциях из JSON-файла"
            "\n2. Получить информацию о транзакциях из CSV-файла"
            "\n3. Получить информацию о транзакциях из XLSX-файла\n\n"
        )

    @patch("builtins.input", return_value="1")
    def test_validate_choice(self, mock_input: Mock) -> None:
        result = validate_choice()
        assert result == 1
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=["hi", "", "-1", "0", "4", "2"])
    def test_invalid_validate_choice(self, mock_input: Mock) -> None:
        result = validate_choice()
        assert result == 2
        assert mock_input.call_count == 6

    @pytest.mark.parametrize(
        "input_data, res", [("executed", "EXECUTED"), ("canceled", "CANCELED"), ("pending", "PENDING")]
    )
    def test_validate_transact_status(self, input_data: str, res: str) -> None:
        with patch("builtins.input", return_value=input_data):
            result = validate_transact_status()
            assert result == res

    @patch("builtins.input", side_effect=["aloha", "", "113", "-@", "executed"])
    def test_invalid_validate_transact_status(self, mock_input: Mock) -> None:
        result = validate_transact_status()
        assert result == "EXECUTED"
        assert mock_input.call_count == 5

    @pytest.mark.parametrize(
        "input_user, input_data, res, expectation",
        [
            (["да", "по возрастанию"], SORT_BY_DATE_NO_SORT, SORT_BY_DATE_ASCENDING, does_not_raise()),
            (["да", "по убыванию"], SORT_BY_DATE_NO_SORT, SORT_BY_DATE_DESCENDING, does_not_raise()),
            (["нет"], SORT_BY_DATE_NO_SORT, SORT_BY_DATE_NO_SORT, does_not_raise()),
            (["да", "по возрастанию"], [], [], does_not_raise()),
            (["да", "по убыванию"], [], [], does_not_raise()),
            (["нет"], [], [], does_not_raise()),
            (["да", "по возрастанию"], [1, [2, ""]], None, pytest.raises(AttributeError)),
            (["да", "по убыванию"], [1, [2, ""]], None, pytest.raises(AttributeError)),
        ],
    )
    def test_ask_sort_by_date(
        self, input_user: list[str], input_data: list[dict], res: list[dict], expectation: ContextManager
    ) -> None:
        with expectation:
            with patch("builtins.input", side_effect=input_user):
                result = ask_sort_by_date(input_data)
                assert result == res

    @pytest.mark.parametrize(
        "input_user, input_data, res, expectation",
        [
            ("да", ALL_CURRENCY_TRANSACTIONS, RUB_CURRENCY_TRANSACTIONS, does_not_raise()),
            ("нет", ALL_CURRENCY_TRANSACTIONS, ALL_CURRENCY_TRANSACTIONS, does_not_raise()),
            ("да", [], [], does_not_raise()),
            ("нет", [], [], does_not_raise()),
            ("да", ["", [1, 2, 3]], None, pytest.raises(AttributeError)),
        ],
    )
    def test_ask_filter_by_currency(
        self, input_user: str, input_data: list[dict], res: list[dict], expectation: ContextManager
    ) -> None:
        with expectation:
            with patch("builtins.input", return_value=input_user):
                result = ask_filter_by_currency(input_data)
                assert result == res

    @pytest.mark.parametrize(
        "input_user, input_data, res, expectation",
        [
            (["Да", "открытие"], TRANSACTIONS_FILTER_NO_QUERY, TRANSACTIONS_FILTER_BY_QUERY_OPENING, does_not_raise()),
            (["ДА", "перевод"], TRANSACTIONS_FILTER_NO_QUERY, TRANSACTIONS_FILTER_BY_QUERY_TRANSFER, does_not_raise()),
            (["нет"], TRANSACTIONS_FILTER_NO_QUERY, TRANSACTIONS_FILTER_NO_QUERY, does_not_raise()),
            (["ДА", "перевод"], [], [], does_not_raise()),
            (["нет"], [], [], does_not_raise()),
            (["да", "рука Сканлана"], TRANSACTIONS_FILTER_NO_QUERY, [], does_not_raise()),
            (["да", "перевод"], ["", [1, 2, 3]], [], does_not_raise()),
        ],
    )
    def test_ask_filter_by_query(
        self, input_user: list[str], input_data: list[dict], res: list[dict], expectation: ContextManager
    ) -> None:
        with expectation:
            with patch("builtins.input", side_effect=input_user):
                result = ask_filter_by_query(input_data)
                assert result == res

    def test_apply_user_filters(self) -> None:
        with patch("src.transactions_utils.ask_sort_by_date", return_value=SAMPLE_TRANSACTIONS):
            with patch("src.transactions_utils.ask_filter_by_currency", return_value=SAMPLE_TRANSACTIONS):
                with patch("src.transactions_utils.ask_filter_by_query", return_value=SAMPLE_TRANSACTIONS):
                    result = apply_user_filters(SAMPLE_TRANSACTIONS)
                    assert result == SAMPLE_TRANSACTIONS

    @patch("src.transactions_utils.ask_sort_by_date", return_value=[{"id": 1}])
    @patch("src.transactions_utils.ask_filter_by_currency", return_value=[{"id": 2}])
    @patch("src.transactions_utils.ask_filter_by_query", return_value=[{"id": 3}])
    def test_apply_user_filters_chain(self, mock_q: Mock, mock_currency: Mock, mock_sort: Mock) -> None:
        result = apply_user_filters([{"id": 0}])
        assert result == [{"id": 3}]
        mock_q.assert_called()
        mock_currency.assert_called()
        mock_sort.assert_called()

    @patch("src.transactions_utils.ask_sort_by_date", return_value=[])
    @patch("src.transactions_utils.ask_filter_by_currency", return_value=[])
    @patch("src.transactions_utils.ask_filter_by_query", return_value=[])
    def test_apply_user_filters_empty_list(self, mock_q: Mock, mock_currency: Mock, mock_sort: Mock) -> None:
        result = apply_user_filters([])
        assert result == []
        mock_q.assert_called()
        mock_currency.assert_called()
        mock_sort.assert_called()

    def test_show_opening_a_deposit(self, capsys: pytest.CaptureFixture) -> None:
        show_opening_a_deposit(OPENING_DEPOSIT)
        captured = capsys.readouterr()
        assert captured.out == ("23.03.2018 Открытие вклада\n" "Счет **2431\n" "Сумма: 48223.05 руб.\n")

    def test_show_transfer(self, capsys: pytest.CaptureFixture) -> None:
        show_transfer(TRANSFER_TRANSACTIONS)
        captured = capsys.readouterr()
        assert captured.out == (
            "26.08.2019 Перевод организации\n" "Maestro 1596 83** **** 5199 -> Счет **9589\n" "Сумма: 31957.58 руб.\n"
        )

    @pytest.mark.parametrize(
        "input_data, res, expectation",
        [
            ([OPENING_DEPOSIT], PRINT_OUT, does_not_raise()),
            ([TRANSFER_TRANSACTIONS], PRINT_OUT, does_not_raise()),
        ],
    )
    def test_print_transactions(
        self, input_data: list[dict], res: str, expectation: ContextManager, capsys: pytest.CaptureFixture
    ) -> None:
        with expectation:
            with patch("src.transactions_utils.show_transfer"):
                with patch("src.transactions_utils.show_opening_a_deposit"):
                    print_transactions(input_data)
                    captured = capsys.readouterr()
                    assert captured.out == res

    def test_empty_print_transactions(self, capsys: pytest.CaptureFixture) -> None:
        print_transactions([])
        captured = capsys.readouterr()
        assert captured.out == "\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.\n"
