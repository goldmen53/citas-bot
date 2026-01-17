"""
Обработка блокирующих состояний (слишком много запросов, редирект и т.д.).
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RestartLoop(Exception):
    """
    Исключение для сигнализации о необходимости перезагрузить цикл поиска.
    Используется вместо break/continue для более явного управления потоком.
    """
    pass


def guard_blocking_states(driver, start_url):
    """
    Обнаруживает и обрабатывает блокирующие состояния сайта.
    
    Блокирующие состояния:
    - 429 Too Many Requests (слишком много запросов)
    - Редирект на страницу с кнопкой "Go Back" (вернуться)
    
    Args:
        driver: WebDriver объект
        start_url: Исходный URL для перезагрузки при блокировке
    
    Returns:
        True если обнаружено блокирующее состояние и произведена обработка
        False если всё в порядке, можно продолжать
    """
    
    # Проверка на 429 Too Many Requests
    if "429" in driver.page_source or "Too Many Requests" in driver.page_source:
        logger.warning("🚫 Обнаружена ошибка 429 Too Many Requests")
        logger.info("⏳ Жду 310 секунд перед перезагрузкой...")
        
        # Показываем прогресс каждые 30 секунд
        for i in range(31):
            if i % 10 == 0 and i > 0:
                logger.info(f"   Ещё {310 - i*10} секунд...")
            time.sleep(10)
        
        logger.info("↻ Перезагружаю страницу...")
        driver.get(start_url)
        time.sleep(2)
        return True
    
    # Проверка на редирект с кнопкой "Go Back"
    try:
        go_back_button = driver.find_element(By.XPATH, "//input[@value='Go Back']")
        logger.warning("🚫 Обнаружена страница блокировки с кнопкой 'Go Back'")
        logger.info("⏳ Жду 610 секунд перед перезагрузкой...")
        
        # Ждём 610 секунд (показываем прогресс каждые 30 секунд)
        for i in range(61):
            if i % 10 == 0 and i > 0:
                logger.info(f"   Ещё {610 - i*10} секунд...")
            time.sleep(10)
        
        logger.info("↻ Перезагружаю страницу...")
        driver.get(start_url)
        time.sleep(2)
        return True
    
    except NoSuchElementException:
        # Кнопка не найдена - всё в порядке
        return False
    
    except Exception as e:
        logger.error(f"⚠️ Ошибка при проверке блокирующих состояний: {e}")
        return False
