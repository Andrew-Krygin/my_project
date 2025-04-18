from src.widget import mask_account_card


def main() -> None:
    """
    Основная функция программы.
    1. Запрашивает у пользователя тип карты/счета и номер.
    2. Маскирует корректные данные в соответствии с требованиями.
    3. Выводит замаскированные номера на экран.
    4. Обрабатывает возможные ошибки.
    """
    while True:
        try:
            payment_identifier = input("Введите тип карты/счета и номер: ").strip().title()
            result = mask_account_card(payment_identifier)
            print(f"Результат: {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

        again = input("Хотите повторить процедуру? (да/нет): ")
        if again.lower() != 'да':
            break


if __name__ == "__main__":
    main()
