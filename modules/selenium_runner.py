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
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

# SeleniumBase for undetected Chrome (uc=True) to bypass anti-bot detection
from seleniumbase import Driver

from modules.nie_specified import NIESpecified
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Глобальный executor для управления потоками
executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="selenium_")


def setup_webdriver():
    """
    Создает SeleniumBase Driver с uc=True (Undetected ChromeDriver).
    
    uc=True использует undetected-chromedriver для маскировки Selenium
    и обхода anti-bot защиты испанского сайта.
    
    Returns:
        seleniumbase.Driver: Настроенный SeleniumBase драйвер
    
    Raises:
        WebDriverException: Если Chrome не установлен или не найден
    """
    try:
        logger.info("🚀 Создаю SeleniumBase Driver (uc=False - видимый браузер для отладки)")
        
        # uc=False - отключаем stealth mode чтобы видеть браузер и отлаживать
        # headless=False - браузер будет видимым
        driver = Driver(
            uc=False,           # Отключено для отладки - видимый браузер
            headless=False,     # Показать интерфейс браузера
            window_size=(1280, 1024),  # Размер окна браузера
            no_sandbox=True,    # Отключить sandbox для стабильности
            disable_gpu=True    # Отключить GPU
        )
        
        logger.info("✅ SeleniumBase Driver успешно создан (видимый браузер для отладки)")
        logger.info("🔍 Браузер видимый - вы можете видеть все действия")
        
        return driver
        
    except WebDriverException as e:
        logger.error(f"❌ Ошибка создания SeleniumBase Driver: {e}")
        logger.error("💡 Решение: pip install seleniumbase>=4.20.0 undetected-chromedriver>=3.5.4")
        raise
    except Exception as e:
        logger.error(f"⚠️ Неожиданная ошибка при создании Driver: {e}")
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
        
        # Импортировать START_URL из config
        from config.xpaths import START_URL
        
        # ВАЖНО: Используем uc_open_with_reconnect для правильной инициализации
        # Это метод SeleniumBase, который автоматически переподключается при блокировке
        logger.info(f"🔌 Открываю URL с автоматическим переподключением: {START_URL}")
        try:
            driver.uc_open_with_reconnect(START_URL, 5)  # 5 попыток переподключения
            logger.info("✅ Страница загружена успешно с помощью uc_open_with_reconnect")
        except Exception as uc_error:
            logger.warning(f"⚠️ uc_open_with_reconnect вернул ошибку: {uc_error}")
            logger.info("Пытаюсь альтернативным способом через .get()...")
            driver.get(START_URL)
        
        # Выбрать правильный класс в зависимости от типа визы
        if visa_type == 'visa_nie_spec':
            logger.info("📋 Тип: НИЕ (с указанием региона)")
            
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
            import time
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
            import time
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
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Ошибка при поиске: {error_msg}")
        logger.exception("Exception occurred")  # Логировать полный stack trace
        
        # Проверяем специфичные ошибки
        if "429" in error_msg or "Too Many Requests" in error_msg:
            message = "⛔ БЛОКИРОВКА: Сайт заблокировал доступ (429)\n⏳ Подожди 10 минут и попробуй снова"
        elif "Connection refused" in error_msg or "no such element" in error_msg or "Timeout" in error_msg:
            message = "❌ Ошибка при взаимодействии с сайтом\nПопробуй позже или проверь соединение"
        else:
            message = f'❌ Ошибка при поиске:\n{error_msg[:200]}'
        
        return {
            'success': False,
            'citations': [],
            'message': message,
            'error': error_msg
        }
    
    except KeyboardInterrupt:
        logger.warning("\n⚠️ ПОИСК ОСТАНОВЛЕН ПОЛЬЗОВАТЕЛЕМ (Ctrl+C)")
        if driver:
            try:
                driver.quit()
                logger.info("🔚 WebDriver закрыт")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при закрытии WebDriver: {e}")
        return {
            'success': False,
            'citations': [],
            'message': '⚠️ Поиск остановлен пользователем (Ctrl+C)',
            'error': 'user_interrupted'
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
