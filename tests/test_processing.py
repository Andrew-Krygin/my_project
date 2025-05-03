import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    @pytest.mark.parametrize("state, count", [('EXECUTED', 3), ("CANCELED", 3), ("PENDING", 0),])
    def test_valid_filter_by_state(self, sample_data: list, state: str, count: int) -> None:
        result = filter_by_state(sample_data, state)
        assert len(result) == count

    @pytest.mark.parametrize("state", [('EXECUTED',), ("CANCELED",), (),])
    def test_empty_filter_by_state(self, empty_data: list, state: str) -> None:
        result = filter_by_state(empty_data, state)
        assert result == []

    @pytest.mark.parametrize(
        "expectation",
        [
            pytest.raises(AttributeError),
            pytest.raises(AttributeError),
            pytest.raises(AttributeError),
        ]
    )
    def test_invalid_filter_by_state(self, invalid_type_data: list, expectation) -> None:
        with expectation:
            assert filter_by_state(invalid_type_data)


# Тесты на работу функции с некорректными или нестандартными форматами дат.
class TestSortByDate:
    @pytest.mark.parametrize(
        "reverse, expected_res",
        [   # Сортировка для reverse=True
            (True,
             [
                 {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                 {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                 {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                 {'id': 615414851, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                 {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                 {'id': 41428829, 'state': 'EXECUTED'},
             ]
             ),

            # Сортировка для reverse=False
            (False,
             [
                 {'id': 41428829, 'state': 'EXECUTED'},
                 {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                 {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                 {'id': 615414851, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                 {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                 {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
             ]
             ),
        ]
    )
    def test_valid_sort_by_date(self, sample_data: list, reverse: bool, expected_res: list) -> None:
        result = sort_by_date(sample_data, reverse)
        assert result == expected_res

    @pytest.mark.parametrize(
        "reverse, expected_res",
        [
            (True, [{}, {}, {}]),
            (False, [{}, {}, {}]),
        ]
    )
    def test_empty_sort_by_date(self, empty_data: list, reverse: bool, expected_res: list) -> None:
        result = sort_by_date(empty_data, reverse)
        assert result == expected_res

    @pytest.mark.parametrize(
        "reverse, expectation",
        [   # Тест для reverse=True
            (True, pytest.raises(TypeError)),

            # Тест для reverse=False
            (False, pytest.raises(TypeError)),
        ]
    )
    def test_invalid_sort_by_date(self, invalid_date_data: list, reverse: bool, expectation) -> None:
        with expectation:
            assert sort_by_date(invalid_date_data, reverse)
