"""
Модуль логирования для проекта CITAS.
Настраивает единый логгер для всех компонентов.
"""

import logging
import logging.handlers
from pathlib import Path

# Создание директории для логов
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Конфигурация логгера
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Настраивает логгер для модуля.
    
    Args:
        name: Имя логгера (обычно __name__ модуля)
        level: Уровень логирования (по умолчанию INFO)
    
    Returns:
        Настроенный logger объект
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Форматтер
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # Обработчик для файла
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "citas.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Главный логгер
logger = setup_logger("CITAS")
