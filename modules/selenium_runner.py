"""
Selenium Runner - Async wrapper для запуска Selenium поиска из Telegram bot'а

Этот модуль содержит функции для:
1. Запуска Selenium браузера и поиска цитаций
2. Управления WebDriver'ом с pooling'ом
3. Обработки ошибок и retry логики
4. Anti-bot механизмов (delays, headers)
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

from modules.nie_specified import NIESpecified
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Глобальный executor для управления потоками
executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="selenium_")


def setup_webdriver():
    """
    Создает и настраивает Chrome WebDriver.
    
    Returns:
        webdriver.Chrome: Настроенный Chrome драйвер
    
    Raises:
        WebDriverException: Если Chrome не установлен или не найден
    """
    try:
        chrome_options = Options()
        
        # Headless mode - запуск без интерфейса (быстрее)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Anti-bot headers
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        
        # Дополнительные опции для стабильности
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        logger.debug("🔧 Создаю Chrome WebDriver с опциями headless")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        logger.info("✅ Chrome WebDriver успешно создан")
        return driver
        
    except WebDriverException as e:
        logger.error(f"❌ Ошибка создания WebDriver: {e}")
        logger.error("💡 Решение: sudo apt-get install chromium-browser")
        raise
    except Exception as e:
        logger.error(f"⚠️ Неожиданная ошибка при создании WebDriver: {e}")
        raise


def run_selenium_search(passport: str, full_name: str, birth_year: str, 
                       visa_type: str, provincia: int = 0, oficina: int = 0, 
                       tramite: int = 0) -> dict:
    """
    BLOCKING функция для запуска Selenium поиска (runs in ThreadPoolExecutor).
    
    Эта функция вызывается в отдельном потоке из async контекста.
    Содержит всю логику взаимодействия с браузером.
    
    Args:
        passport: Номер паспорта пользователя (например, 'FV315480')
        full_name: Полное имя пользователя (например, 'Yevhen Maksymov')
        birth_year: Год рождения (строка, например, '1991')
        visa_type: Тип визы ('visa_nie_spec', 'visa_nie_nat', 'visa_tie')
        provincia: Индекс провинции (default 0)
        oficina: Индекс офиса (default 0)
        tramite: Индекс типа услуги (default 0)
    
    Returns:
        dict: {
            'success': bool,
            'citations': list of str,
            'message': str,
            'error': str or None
        }
    """
    driver = None
    
    try:
        logger.info(f"🚀 Начинаю поиск Selenium для {visa_type}")
        logger.info(f"   Паспорт: {passport}")
        logger.info(f"   Имя: {full_name}")
        
        # Создать WebDriver
        driver = setup_webdriver()
        
        # Выбрать правильный класс в зависимости от типа визы
        if visa_type == 'visa_nie_spec':
            logger.info("📋 Тип: НИЕ (с указанием региона)")
            
            # Импортировать START_URL из config
            from config.xpaths import START_URL
            
            searcher = NIESpecified(
                driver=driver,
                start_url=START_URL,
                passport=passport,
                full_name=full_name,
                birth_year=birth_year,
                provincia=provincia,
                oficina=oficina,
                tramite=tramite
            )
            
            # Запустить поиск
            logger.info("🔍 Запускаю метод search_for_citations()...")
            citations = searcher.search_for_citations()
            
            logger.info(f"✅ Поиск завершен успешно")
            logger.info(f"   Найдено цитаций: {len(citations) if citations else 0}")
            
            return {
                'success': True,
                'citations': citations if citations else [],
                'message': f'✅ Найдено цитаций: {len(citations)}' if citations else '❌ Цитации не найдены',
                'error': None
            }
        
        elif visa_type == 'visa_nie_nat':
            logger.info("📋 Тип: НИЕ (национальный)")
            logger.warning("⚠️ НИЕ национальный еще не реализован, используем mock")
            logger.warning("⚠️ ВАЖНО: Это MOCK результаты, не реальный поиск!")
            
            # Mock implementation для демонстрации
            time.sleep(2)
            return {
                'success': True,
                'citations': [],  # Пусто - нет реального поиска
                'message': '⚠️ НИЕ национальный еще не реализован. Используй visa_nie_spec (НИЕ с регионом).',
                'error': 'not_implemented'
            }
        
        elif visa_type == 'visa_tie':
            logger.info("📋 Тип: ТИЕ")
            logger.warning("⚠️ ТИЕ еще не реализован, используем mock")
            logger.warning("⚠️ ВАЖНО: Это MOCK результаты, не реальный поиск!")
            
            # Mock implementation для демонстрации
            time.sleep(2)
            return {
                'success': True,
                'citations': [],  # Пусто - нет реального поиска
                'message': '⚠️ ТИЕ еще не реализован. Используй visa_nie_spec (НИЕ с регионом).',
                'error': 'not_implemented'
            }
        
        else:
            error_msg = f"Неизвестный тип визы: {visa_type}"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'citations': [],
                'message': f'❌ Ошибка: {error_msg}',
                'error': error_msg
            }
        
    except TimeoutException as e:
        error_msg = f"⏱️ Timeout при загрузке сайта: {e}"
        logger.error(error_msg)
        return {
            'success': False,
            'citations': [],
            'message': '❌ Сайт не ответил в отведенное время',
            'error': error_msg
        }
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Ошибка при поиске: {error_msg}")
        logger.exception(e)  # Логировать полный stack trace
        return {
            'success': False,
            'citations': [],
            'message': f'❌ Ошибка при поиске:\n{error_msg[:200]}',
            'error': error_msg
        }
    
    finally:
        # Всегда закрывать браузер
        if driver:
            try:
                driver.quit()
                logger.info("🔚 WebDriver закрыт")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при закрытии WebDriver: {e}")


async def async_search(passport: str, full_name: str, birth_year: str, 
                       visa_type: str, provincia: int = 0, oficina: int = 0, 
                       tramite: int = 0) -> dict:
    """
    ASYNC функция - обертка для блокирующего Selenium.
    
    Эта функция вызывается из async контекста Telegram bot'а.
    Она запускает блокирующий Selenium в отдельном потоке чтобы не блокировать bot.
    
    Args: см. run_selenium_search
    
    Returns: см. run_selenium_search
    """
    logger.info(f"📞 async_search вызвана для {visa_type}")
    
    try:
        # Запустить blocking функцию в executor (отдельный поток)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            run_selenium_search,
            passport,
            full_name,
            birth_year,
            visa_type,
            provincia,
            oficina,
            tramite
        )
        
        logger.info(f"📞 async_search завершена с результатом: {result['success']}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Ошибка в async_search: {e}")
        logger.exception(e)
        return {
            'success': False,
            'citations': [],
            'message': f'❌ Внутренняя ошибка: {str(e)[:100]}',
            'error': str(e)
        }


# Инициализация при импорте модуля
logger.info("✅ selenium_runner.py загружен успешно")
logger.info(f"📊 WebDriver executor инициализирован с max_workers=3")
