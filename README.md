
# my_project

## Описание проекта
Проект представляет собой банковский виджет, который показывает несколько последних успешных банковских операций 
клиента.


## Структура проекта

- `src/masks` - модуль, содержащий функции для маскировки данных (например, номеров карт и счетов), чтобы защитить
конфиденциальность пользователя.
- `src/widget` - модуль, который проверяет входные данные, маскирует их при необходимости, и форматирует 
дату в удобочитаемый вид.
- `src/processing` - модуль содержит функции для обработки списка словарей.
- `src/generators` - модуль содержит функции для работы с транзакциями и генерацией номеров карт.
- `src/decorators` - модуль с универсальным логирующим декоратором `@log`, который отслеживает вызовы, аргументы, 
результат выполнения и исключения. Поддерживает логирование как в консоль, так и в файл.


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

- ### `filter_by_currency()`
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

- ### `transaction_descriptions()`
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

- ### `card_number_generator()`
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

- ### Декоратор `@log()`
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
- Покрываются модули `src/masks`, `src/processing`, `src/widget`, `src/decorators`.

## Авторы
- [Andrew Krygin](https://github.com/Andrew-Krygin)
