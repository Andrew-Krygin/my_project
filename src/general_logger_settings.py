import logging
from pathlib import Path
from typing import Literal

# Объявляем тип для уровня логирования:
# Это может быть либо число (например, logging.INFO == 20), либо строка — "INFO", "DEBUG" и т.п.
LogLevel = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logger(
    name: str,
    level: LogLevel = "INFO",
    log_file: str | None = None,
    log_to_console: bool = False,
    fmt: str = "%(asctime)s [%(levelname)-5s] logger:%(name)s module:%(module)s func:%(funcName)s:%(lineno)d - %("
    "message)s",
) -> logging.Logger:
    """
    Универсальная настройка логгера.

    :param name: Имя логгера (обычно __name__)
    :param level: уровень логирования (по умолчанию INFO)
    :param log_file: путь к лог-файлу (если нужно логировать в файл)
    :param log_to_console: по умолчанию не создается (если нужно логировать в консоль)
    :param fmt: формат сообщения
    :return: настроенный логгер
    """

    # Получаем логгер с указанным именем.
    logger = logging.getLogger(name)

    # Устанавливаем уровень логирования (INFO по умолчанию).
    logger.setLevel(level)

    # Создаём форматтер с шаблоном вывода логов.
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    # Создаем handler для вывода в консоль.
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Создаем handler для вывода в файл.
    if log_file:
        logs_dir = Path(__file__).resolve().parent.parent / "logs"
        log_path = logs_dir / log_file

        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Возвращаем полностью настроенный логгер.
    return logger
