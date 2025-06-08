from src.general_logger_settings import setup_logger
from src.processing import filter_by_state
from src.transactions_utils import (LOAD_FILE, MENU_ITEMS, apply_user_filters, print_transactions, show_menu,
                                    validate_choice, validate_transact_status)

main_logger = setup_logger(__name__, log_file="main.log")


def main() -> None:
    """
    Основная функция программы, обеспечивающая взаимодействие с пользователем и связывающая функциональности
    обработки банковских транзакций.

    Поведение функции:

    1. Приветствует пользователя и выводит меню выбора источника данных (JSON, CSV, XLSX).
    2. Запрашивает у пользователя выбор статуса транзакций для фильтрации.

       - Обрабатывает ввод без учёта регистра (например, 'executed', 'Executed' и 'EXECUTED' считаются одинаковыми).
       - В случае неверного ввода повторно запрашивает корректный статус без прерывания работы.
    3. Предлагает дополнительные опции для уточнения выборки:

       - Сортировка по дате (возрастание/убывание).
       - Фильтрация по валюте (только рублевые транзакции или все).
       - Фильтрация по слову в описании.
    4. Выводит итоговый список транзакций, соответствующий выбранным фильтрам и сортировкам.

       - Если выборка пустая, информирует пользователя об отсутствии подходящих транзакций.

    :return: None
    """
    while True:
        main_logger.info("Программа начинает свое выполнение.")
        try:
            main_logger.info("Вывод меню на экран.")
            # Меню программы.
            show_menu()

            main_logger.info("Пользователь выбирает пункт меню.")
            # Выбор пользователем пункта меню и проверка на корректность.
            correct_choice = validate_choice()
            print(MENU_ITEMS.get(correct_choice))

            main_logger.info("Загружается список транзакций из выбранного файла.")
            # Загружаем список транзакций из файла выбранного формата.
            transactions = LOAD_FILE[correct_choice]()

            # Выбор пользователем статуса по которому фильтруются транзакции и его проверка на корректность.
            correct_status = validate_transact_status()

            main_logger.info("Осуществляется фильтрация транзакций по выбранному статусу.")
            # Получаем список транзакций по выбранному статусу.
            transactions = filter_by_state(transactions, correct_status)
            print(f"Операции отфильтрованы по статусу {correct_status}.\n")

            main_logger.info("Осуществляется фильтрация транзакций по дате, валюте, поисковому слову.")
            transactions = apply_user_filters(transactions)

            print("-" * len("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "))

            # Выводим результат фильтрации списка транзакций на экран.
            main_logger.info("Выводим отфильтрованный список транзакций на экран.")
            print_transactions(transactions)
            main_logger.info(f"Финальный список содержит {len(transactions)} транзакций.")
            print()
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
