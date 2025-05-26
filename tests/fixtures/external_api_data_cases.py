VALID_DATA_RUB_EXTERNAL_API = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589",
}

VALID_DATA_USD_EXTERNAL_API = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {"amount": "3234.58", "currency": {"name": "USD", "code": "USD"}},
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589",
}

INVALID_INPUTS_CASES_EXTERNAL_API = [
    (123, 0.0),
    ([1, 2, 3], 0.0),
    ("hi my mentor", 0.0),
    (False, 0.0),
]


EMPTY_VALUES_IN_DICT_EXTERNAL_API = [
    ({"currency": None, "amount": 100}, 0.0),
    ({"currency": "RUB", "amount": None}, 0.0),
    ({"currency": None, "amount": None}, 0.0),
]

INVALID_AMOUNT_EXTERNAL_API = [
    ({"operationAmount": {"amount": ""}}, 0.0),
    ({"operationAmount": {"amount": "Something"}}, 0.0),
    ({"operationAmount": {"amount": [1, 2]}}, 0.0),
    ({"operationAmount": {"amount": {"Something": "wrong"}}}, 0.0),
    ({"operationAmount": {"amount": None}}, 0.0),
]
