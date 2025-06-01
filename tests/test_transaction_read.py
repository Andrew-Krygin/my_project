from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.transaction_read import transaction_read_csv, transaction_read_xlsx


class TestTransactionRead:
    def test_transaction_read_csv(self, data_for_read_csv_xlsx: list[dict]) -> None:
        mock_df = pd.DataFrame(data_for_read_csv_xlsx)

        with patch("src.transaction_read.pd.read_csv", return_value=mock_df) as mock_data:
            mock_path = MagicMock(spec=Path)
            result = transaction_read_csv(mock_path)
            assert result == data_for_read_csv_xlsx
            mock_data.assert_called_once()

    @pytest.mark.parametrize(
        "invalid_path",
        [
            "invalid_path",
            1234,
            [],
            None,
            "",
        ],
    )
    def test_invalid_path_transaction_read_csv(self, invalid_path: Any) -> None:
        with pytest.raises(ValueError):
            transaction_read_csv(invalid_path)  # type: ignore

    def test_file_not_found_transaction_read_csv(self) -> None:
        mock_path = MagicMock(spec=Path)
        with patch("src.transaction_read.pd.read_csv", side_effect=FileNotFoundError) as mock_except:
            with pytest.raises(FileNotFoundError):
                transaction_read_csv(mock_path)
            mock_except.assert_called_once()

    def test_empty_csv_file(self) -> None:
        mock_df = pd.DataFrame()
        with patch("src.transaction_read.pd.read_csv", return_value=mock_df):
            mock_path = MagicMock(spec=Path)
            result = transaction_read_csv(mock_path)
            assert result == []

    def test_transaction_read_xlsx(self, data_for_read_csv_xlsx: list[dict]) -> None:
        mock_df = pd.DataFrame(data_for_read_csv_xlsx)

        with patch("src.transaction_read.pd.read_excel", return_value=mock_df) as mock_data:
            mock_path = MagicMock(spec=Path)
            result = transaction_read_xlsx(mock_path)
            assert result == data_for_read_csv_xlsx
            mock_data.assert_called_once()

    @pytest.mark.parametrize(
        "invalid_path",
        [
            "invalid_path",
            1234,
            [],
            None,
            "",
        ],
    )
    def test_invalid_path_transaction_read_xlsx(self, invalid_path: Any) -> None:
        with pytest.raises(ValueError):
            transaction_read_xlsx(invalid_path)  # type: ignore

    def test_file_not_found_transaction_read_xlsx(self) -> None:
        mock_path = MagicMock(spec=Path)
        with patch("src.transaction_read.pd.read_excel", side_effect=FileNotFoundError) as mock_except:
            with pytest.raises(FileNotFoundError):
                transaction_read_xlsx(mock_path)
            mock_except.assert_called_once()

    def test_empty_xlsx_file(self) -> None:
        mock_df = pd.DataFrame()
        with patch("src.transaction_read.pd.read_excel", return_value=mock_df):
            mock_path = MagicMock(spec=Path)
            result = transaction_read_xlsx(mock_path)
            assert result == []
