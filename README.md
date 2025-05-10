
# my_project

## Описание проекта
Проект включает в себя банковский виджет, который показывает несколько последних успешных банковских операций клиента.


## Структура проекта

- `src/masks` - модуль, содержащий функции для маскировки данных (например, номеров карт и счетов), чтобы защитить
конфиденциальность пользователя.
- `src/widget` - модуль, который проверяет входные данные, маскирует их при необходимости, и преобразует дату 
в нужный формат.
- `src/processing` - модуль содержит функции для обработки списка словарей.
- `src/generators` - модуль содержит функции для работы с транзакциями и генерацией номеров карт.


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
### Функции модуля generators.

- filter_by_currency
```bash
   def filter_by_currency(lst_transactions: list[dict], currency: str) -> Iterator[dict]
```
Фильтрует список транзакций, возвращая только те, в которых указана заданная валюта.

#### Пример:
```bash
   from src.generators import filter_by_currency
    
    transactions = [
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

- transaction_descriptions
```bash
   def transaction_descriptions(transactions: list[dict]) -> Iterator[str]
```
Извлекает описания транзакций из списка словарей.

#### Пример:
```bash
   descriptions = list(transaction_descriptions(transactions))
```
#### Вывод:

```
["Перевод организации", "Перевод со счета на счет"]
```

- card_number_generator

```bash
   def card_number_generator(start: int, stop: int) -> Iterator[str]
```
Генерирует номера карт от start до stop в формате XXXX XXXX XXXX XXXX.

#### Пример:
```bash
   card = list(card_number_generator(1, 3))
```

#### Вывод:
```
['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']
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
- Фикстуры и тестовые кейсы вынесены в `tests/conftest.py`.
- Покрываются модули `src/masks`, `src/processing`, `src/widget`.

## Авторы
- [Andrew Krygin](https://github.com/Andrew-Krygin)
