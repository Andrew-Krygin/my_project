import json
from typing import ContextManager
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.utils import load_transactions
from tests.fixtures.utils_cases import INVALID_DATA_UTILS, INVALID_INPUTS_AND_EXCEPTIONS_CASES_UTILS, VALID_DATA_UTILS

json_valid_data_str = json.dumps(VALID_DATA_UTILS)
json_invalid_data_str = json.dumps(INVALID_DATA_UTILS)


class TestUtils:
    def test_valid_load_transactions(self) -> None:
        with patch("builtins.open", mock_open(read_data=json_valid_data_str)) as mock_file:
            with patch("json.load", return_value=VALID_DATA_UTILS) as mock_json_load:
                result = load_transactions("fake/path.json")
                assert result == VALID_DATA_UTILS
                mock_json_load.assert_called_once()
                mock_file.assert_called_once_with("fake/path.json", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data=json_invalid_data_str)
    def test_load_transactions_not_list(self, mock_file: MagicMock) -> None:
        with patch("json.load", return_value="Not a list.") as mock_json_load:
            result = load_transactions("fake/path.json")
            assert result == []
            mock_file.assert_called_once_with("fake/path.json", encoding="utf-8")
            mock_json_load.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_load_transactions_empty_list(self, mock_file: MagicMock) -> None:
        with patch("json.load", return_value=[]) as mock_json_load:
            result = load_transactions("fake/path.json")
            assert result == []
            mock_file.assert_called_once_with("fake/path.json", encoding="utf-8")
            mock_json_load.assert_called_once()

    @patch("builtins.open")
    def test_load_transactions_exception_file_not_found(self, mock_open_file: MagicMock) -> None:
        mock_open_file.side_effect = FileNotFoundError("message")
        result = load_transactions("invalid_path.json")
        assert result == []

    @patch("builtins.open")
    def test_load_transactions_exception_json_decode_error(self, mock_open_file: MagicMock) -> None:
        with patch("json.load", side_effect=json.JSONDecodeError("message", "doc", 0)) as mock_json_load:
            result = load_transactions("fake/path.json")
            assert result == []
            mock_json_load.assert_called_once()
            mock_open_file.assert_called_once_with("fake/path.json", encoding="utf-8")

    @pytest.mark.parametrize("input_data, expected_exception", INVALID_INPUTS_AND_EXCEPTIONS_CASES_UTILS)
    def test_load_transactions_invalid_path(self, input_data: list, expected_exception: ContextManager) -> None:
        with expected_exception:
            assert load_transactions(input_data)  # type: ignore
