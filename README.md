# my_project

## Описание проекта
Проект представляет собой банковский виджет, который показывает несколько последних успешных банковских операций 
клиента.

## Структура проекта

- **src/masks**: Модуль для маскировки данных (номера карт, счета и т.д.)
- **src/widget**: Модуль для проверки входных данных, их маскировки и форматирования даты.
- **src/processing**: Модуль для обработки списка словарей.
- **src/generators**: Модуль для работы с транзакциями и генерацией номеров карт.
- **src/decorators**: Модуль с декоратором `@log`, который логирует информацию о вызовах.
- **src/utils**: Модуль для работы с JSON данными и файловыми операциями.
- **src/external_api**: Модуль для работы с транзакциями и конвертацией валют в RUB с использованием внешнего API.
- **src/transaction_read**: Модуль для работы с данными из CSV и XLSX файлов.


## Установка
##### Для пользователя:
1. Установите Poetry, если он ещё не установлен:  
   [Инструкция по установке Poetry](https://python-poetry.org/docs/#installation)

2. Добавьте виджет в свой проект:
   ```bash
   poetry add my_project
   ```

##### Для разработчика:
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Andrew-Krygin/my_project.git
   ```
   
2. Перейдите в каталог проекта:
   ```bash
   cd my_project
   ```
   
3. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```


## Пример использования
### Модуль generators.

### `filter_by_currency()`
```python
from typing import Iterator


def filter_by_currency(lst_transactions: list[dict], currency: str) -> Iterator[dict]:
```
Фильтрует список транзакций, возвращая только те, в которых указана заданная валюта.

#### Пример:
```python
from src.generators import filter_by_currency
    
transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                       "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        }
    ]
    
filtered = list(filter_by_currency(transactions, "USD"))
```
#### Вывод:
```
[
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        }
]
```

### `transaction_descriptions()`
```python
from typing import Iterator

def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
```
Извлекает описания транзакций из списка словарей.

#### Пример:
```python
descriptions = list(transaction_descriptions(transactions))
```
#### Вывод:

```
["Перевод организации", "Перевод со счета на счет"]
```

### `card_number_generator()`
```python
from typing import Iterator


def card_number_generator(start: int, stop: int) -> Iterator[str]:
```
Генерирует номера карт от start до stop включительно в формате XXXX XXXX XXXX XXXX.

#### Пример:
```python
card = list(card_number_generator(1, 3))
```

#### Вывод:
```
['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']
```

### Модуль decorators.

### Декоратор `@log()`
```python
from src.decorators import log
    
@log()
def some_function():
    return 5 
```
Декоратор @log() логирует:
- начало выполнения функции;
- переданные позиционные и именованные аргументы;
- успешное завершение с результатом;
- исключение, если оно возникает, с типом и трассировкой.

#### Пример:
```python
from src.decorators import log
    
@log()  # логирование в консоль
def greet() -> None:
    print("Hello world!")
    
@log(file_name="logs/app.log")  # логирование в файл
def division(x: int, y: int) -> int | float:
    return x / y
```
#### Вывод:
```
2025-05-17 17:46:03 [INFO ] decorators.wrapper:33 - Function greet started with args () and kwargs {}.
2025-05-17 17:46:03 [INFO ] decorators.wrapper:35 - Function greet finished successfully with result: None
```

#### В случае исключения:
```
2025-05-17 17:47:13 [INFO ] decorators.wrapper:33 - Function division started with args (7, 0) and kwargs {}.
2025-05-17 17:47:13 [ERROR] decorators.wrapper:38 - Error in division | Type: ZeroDivisionError | Args: (7, 0) | Kwargs: {}
Traceback (most recent call last):
  File "/Users/andrejkrygin/PycharmProjects/my_project/src/decorators.py", line 34, in wrapper
    result = func(*args, **kwargs)
  File "/Users/andrejkrygin/PycharmProjects/my_project/src/decorators.py", line 49, in division
    return x / y
           ~~^~~
ZeroDivisionError: division by zero
```
### Модуль utils.
### load_transactions(path_to_file: str) -> list:
 Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.

#### Пример:
```python
import json
import os


BASE_DIR = os.path.dirname(__file__)
PATH_TO_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "operations.json")

print(load_transactions(PATH_TO_FILE))
```
#### Вывод:
```
[
  {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  },
  {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  },
]
```
### Модуль external_api.
### def calculate_transaction_to_rub(transaction: dict) -> float:
Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях. 
Если валюта уже RUB — возвращает сумму без обращения к API.
Если валюта отличается, делает запрос к ExchangeRates API для конвертации.

#### Пример:
Если транзакция в рублях.
```python
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


calculate_transaction_to_rub({
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  })
```

#### Вывод:
```
31957.58
```
Если транзакция в USD или EUR.
```python
calculate_transaction_to_rub({
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  })
```

#### Вывод:
```
634531.56
```

### Модуль transaction_read.
### def transaction_read_csv(path_to_file_csv: Path) -> list[dict]:
Читает CSV-файл и возвращает список транзакций в виде словарей.
#### Пример:
```python
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PATH_TO_FILE_CSV = DATA_DIR / "transactions.csv"


print(transaction_read_csv(PATH_TO_FILE_CSV))
```
#### Вывод
```
[
    {
        'id': 650703.0, 
        'state': 'EXECUTED', 
        'date': '2023-09-05T11:30:32Z', 
        'amount': 16210.0, 
        'currency_name': 'Sol', 
        'currency_code': 'PEN', 
        'from': 'Счет 58803664561298323391', 
        'to': 'Счет 39745660563456619397', 
        'description': 'Перевод организации'
    }, 
    {
        'id': 3598919.0, 
        'state': 'EXECUTED', 
        'date': '2020-12-06T23:00:58Z', 
        'amount': 29740.0, 
        'currency_name': 'Peso', 
        'currency_code': 'COP', 
        'from': 'Discover 3172601889670065', 
        'to': 'Discover 0720428384694643', 
        'description': 'Перевод с карты на карту'
    },
]
```
### def transaction_read_xlsx(path_to_file_xlsx: Path) -> list:
Читает XLSX-файл и возвращает список транзакций в виде словарей.
#### Пример:
```python
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PATH_TO_FILE_XLSX = DATA_DIR / "transactions_excel.xlsx"


print(transaction_read_xlsx(PATH_TO_FILE_XLSX))
```
#### Вывод
```
[
    {
        'id': 3176764.0, 
        'state': 'CANCELED', 
        'date': '2022-08-24T14:32:38Z', 
        'amount': 16652.0, 
        'currency_name': 'Euro', 
        'currency_code': 'EUR', 
        'from': 'Mastercard 8387037425051294', 
        'to': 'American Express 5556525473658852', 
        'description': 'Перевод с карты на карту'
    }, 
    {
        'id': 3598919.0, 
        'state': 'EXECUTED', 
        'date': '2020-12-06T23:00:58Z', 
        'amount': 29740.0, 
        'currency_name': 'Peso', 
        'currency_code': 'COP', 
        'from': 'Discover 3172601889670065', 
        'to': 'Discover 0720428384694643', 
        'description': 'Перевод с карты на карту'
    },
]
```

## Тестирование
Проект использует pytest для модульного тестирования и pytest-cov для оценки покрытия кода. 

- Установите необходимые зависимости для разработки:
   ```bash
   poetry add --dev pytest pytest-cov
   ```

### Запуск тестов
- Для запуска всех тестов:
   ```bash
   poetry run pytest
   ```

- Для более подробного вывода:
   ```bash
   poetry run pytest -v
   ```

### Проверка покрытия кода
- Запуск с отображением процента покрытия:
   ```bash
   poetry run pytest --cov=src
   ```

- Для генерации HTML-отчёта покрытия:
   ```bash
   poetry run pytest --cov=src --cov-report=html
   ```

HTML-отчёт будет доступен по пути `htmlcov/index.html`.

### Структура тестов
- Все тесты расположены в директории `tests/`.
- Фикстуры и тестовые кейсы вынесены в папку `tests/fixture/`.
- Покрываются модули `src/masks`, `src/processing`, `src/widget`, `src/decorators`, `src/utils`, 
  `src/external_api`, `src/transaction_read`.

## Авторы
- [Andrew Krygin](https://github.com/Andrew-Krygin)
