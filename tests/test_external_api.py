import json
from typing import Any, cast
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests.exceptions
from _pytest.monkeypatch import MonkeyPatch

from src.external_api import calculate_transaction_to_rub
from tests.fixtures.external_api_data_cases import (EMPTY_VALUES_IN_DICT_EXTERNAL_API, INVALID_AMOUNT_EXTERNAL_API,
                                                    INVALID_INPUTS_CASES_EXTERNAL_API, VALID_DATA_RUB_EXTERNAL_API,
                                                    VALID_DATA_USD_EXTERNAL_API)

json_data_str = json.dumps(VALID_DATA_USD_EXTERNAL_API)


class TestExternalApi:
    def test_calculate_transaction_to_rub(self) -> None:
        result = calculate_transaction_to_rub(VALID_DATA_RUB_EXTERNAL_API)
        assert result == 31957.58

    @pytest.mark.parametrize("input_data, res", INVALID_INPUTS_CASES_EXTERNAL_API)
    def test_calculate_transaction_to_rub_invalid_arg(self, input_data: list, res: float) -> None:
        result = calculate_transaction_to_rub(input_data)  # type: ignore
        assert result == res

    @pytest.mark.parametrize("input_data, res", EMPTY_VALUES_IN_DICT_EXTERNAL_API)
    def test_calculate_transaction_to_rub_empty_values_in_dict(self, input_data: dict, res: float) -> None:
        result = calculate_transaction_to_rub(input_data)
        assert result == res

    @pytest.mark.parametrize("input_data, res", INVALID_AMOUNT_EXTERNAL_API)
    def test_calculate_transaction_to_rub_invalid_amount(self, input_data: dict, res: float) -> None:
        result = calculate_transaction_to_rub(input_data)
        assert result == res

    @patch("requests.get")
    def test_calculate_transaction_to_rub_from_usd(self, mock_get: MagicMock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 257952.08}
        result = calculate_transaction_to_rub(VALID_DATA_USD_EXTERNAL_API)

        assert result == 257952.08
        mock_get.assert_called_once()

    @pytest.mark.parametrize(
        "side_effect", [requests.exceptions.RequestException("message"), json.JSONDecodeError("message", "doc", 0)]
    )
    def test_calculate_transaction_to_rub_api_errors(self, monkeypatch: MonkeyPatch, side_effect: Any) -> None:
        mock_get = Mock()
        mock_get.side_effect = side_effect

        monkeypatch.setattr(requests, "get", mock_get)

        transaction = cast(dict, VALID_DATA_USD_EXTERNAL_API)
        amount = transaction.get("operationAmount", {}).get("amount")
        expected = float(amount)

        result = calculate_transaction_to_rub(VALID_DATA_USD_EXTERNAL_API)
        assert result == expected
        mock_get.assert_called_once()
