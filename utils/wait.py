"""
Утилиты для ожидания элементов на странице.
Содержит функции для безопасного поиска и ожидания загрузки элементов.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import setup_logger

logger = setup_logger(__name__)


def wait_clickable(driver, by, value, timeout=30):
    """
    Ожидает, пока элемент станет кликабельным.
    
    Args:
        driver: WebDriver объект
        by: Тип селектора (By.XPATH, By.ID и т.д.)
        value: Значение селектора
        timeout: Максимальное время ожидания в секундах
    
    Returns:
        WebElement если найден, иначе None
        
    Raises:
        TimeoutException: Если элемент не найден за отведённое время
    """
    try:
        logger.debug(f"Ожидаю элемент {value} (тип: {by})")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        logger.info(f"✓ Элемент найден: {value}")
        return element
    except TimeoutException:
        logger.error(f"✗ Элемент НЕ найден после {timeout}s: {value}")
        raise


def safe_wait_clickable(driver, by, value, timeout=30, default=None):
    """
    Безопасное ожидание (не выбрасывает исключение).
    
    Args:
        driver: WebDriver объект
        by: Тип селектора
        value: Значение селектора
        timeout: Максимальное время ожидания
        default: Значение по умолчанию если элемент не найден
    
    Returns:
        WebElement или значение по умолчанию
    """
    try:
        return wait_clickable(driver, by, value, timeout)
    except TimeoutException:
        logger.warning(f"Используется значение по умолчанию для {value}")
        return default


def wait_for_element(driver, by, value, timeout=30):
    """
    Ожидает, пока элемент будет присутствовать в DOM (не обязательно видимый).
    
    Args:
        driver: WebDriver объект
        by: Тип селектора
        value: Значение селектора
        timeout: Максимальное время ожидания
    
    Returns:
        WebElement если найден
        
    Raises:
        TimeoutException: Если элемент не найден
    """
    try:
        logger.debug(f"Ожидаю присутствие элемента {value}")
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        logger.info(f"✓ Элемент присутствует: {value}")
        return element
    except TimeoutException:
        logger.error(f"✗ Элемент НЕ присутствует: {value}")
        raise
