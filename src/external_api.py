import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def calculate_transaction_to_rub(transaction: dict) -> float:
    """
    Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float.
    Если валюта уже RUB — возвращает сумму без обращения к API.
    Если валюта отличается, делает запрос к ExchangeRates API для конвертации.
    """
    # Проверяем что входящий аргумент это словарь.
    if not isinstance(transaction, dict):
        return 0.0

    # Получаем сумму и валюту.
    target_currency = "RUB"
    amount = transaction.get("operationAmount", {}).get("amount")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    # Проверяем наличие суммы и валюты
    if amount is None or currency is None:
        return 0.0

    # Приводим значение к числовому.
    try:
        float_amount = float(amount)
    except (ValueError, TypeError):
        return 0.0

    # Если валюта RUB - возвращаем сумму без обращения к API.
    if currency == target_currency:
        return float_amount

    # Если валюта не RUB - обращаемся к API.
    if currency in ["USD", "EUR"]:
        # Запрос к API для конвертации валюты в рубли
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": API_KEY}
        params = {"to": target_currency, "from": currency, "amount": float_amount}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if (result := data.get("result")) is not None:
                return round(float(result), 2)
        except requests.exceptions.RequestException as req_err:
            print(f"[HTTP Error]: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"[JSON Decode Error]: {json_err}")

    return round(float_amount, 2)
