import pytest


# Фикстуры используются в модуле test_processing.py
@pytest.fixture
def sample_data() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 41428829, "state": "EXECUTED"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 615414851, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]


@pytest.fixture
def empty_data() -> list[dict]:
    return [
        {},
        {},
        {},
    ]


@pytest.fixture
def invalid_type_data() -> list:
    return [1234, ("aededa",), set()]


@pytest.fixture
def invalid_date_data() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": None},
        {"id": 41428829, "state": "EXECUTED", "date": 1234},
        {"id": 41428829, "state": "CANCELED", "date": "не_дата"},
        {"id": 41428829, "state": "CANCELED"},
    ]
