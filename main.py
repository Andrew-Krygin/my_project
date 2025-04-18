from src.masks import LENGTH_ACCOUNT_NUM, LENGTH_CARD_NUM, data_validation, get_mask_account, get_mask_card_number


def main() -> None:
    """
    Основная функция программы.
    1. Запрашивает у пользователя номер карты и номер счета.
    2. Валидирует введенные данные.
    3. Маскирует корректные данные в соответствии с требованиями.
    4. Выводит замаскированные номера на экран.
    """
    # Запрашиваем у пользователя номер карты, осуществляем валидацию данных и маскируем в соответствии с ТЗ.
    user_card_number = input("Введите номер карты: ")
    correct_card_number = data_validation(user_card_number, LENGTH_CARD_NUM)
    mask_card = get_mask_card_number(correct_card_number)

    # Запрашиваем у пользователя номер счета, осуществляем валидацию данных и маскируем в соответствии с ТЗ.
    user_account_number = input("Введите номер счета: ")
    correct_account_number = data_validation(user_account_number, LENGTH_ACCOUNT_NUM)
    mask_account = get_mask_account(correct_account_number)

    # Выводим результат на экран.
    print(mask_card, mask_account, sep="\n")


if __name__ == "__main__":
    main()