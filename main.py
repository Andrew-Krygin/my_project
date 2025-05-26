from src.general_logger_settings import setup_logger
from src.widget import mask_account_card

main_logger = setup_logger(__name__, log_file="main.log")


def main() -> None:
    """
    Основная функция программы.
    1. Запрашивает у пользователя тип карты/счета и номер.
    2. Маскирует корректные данные в соответствии с требованиями.
    3. Выводит замаскированные номера на экран.
    4. Обрабатывает возможные ошибки.
    """
    while True:
        main_logger.info("Программа начинает свое выполнение.")
        try:
            main_logger.info("Запрашиваются данные карты или счета.")
            payment_identifier = input("Введите тип карты/счета и номер: ").strip().title()
            main_logger.info("Маскируются введенные пользователем данные.")
            result = mask_account_card(payment_identifier)
            print(f"Результат: {result}")
        except ValueError as e:
            main_logger.exception("Ошибка! | Тип: %s", type(e).__name__)
            print(f"Ошибка: {e}")
        except Exception as e:
            main_logger.exception("Ошибка! | Тип: %s", type(e).__name__)
            print(f"Произошла непредвиденная ошибка: {e}")

        again = input("Хотите повторить процедуру? (да/нет): ")
        if again.lower() != "да":
            main_logger.info("Программа завершает свою работу.")
            break
        main_logger.info("Программа продолжает свою работу.")


if __name__ == "__main__":
    main()
