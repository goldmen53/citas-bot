"""
Пример использования модуля NIESpecified.

Этот файл показывает, как инициализировать и запустить поиск цитаций
для НИЕ с указанием региона.
"""

from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from modules.nie_specified import NIESpecified
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Пример запуска поиска цитаций для НИЕ с регионом."""
    
    # Параметры пользователя
    START_URL = 'https://icp.administracionelectronica.gob.es/icpco/index'
    PASSPORT = 'FV315480'
    NAME_SURNAME = 'Yevhen Maksymov'
    B_YEAR = '1991'
    PROVINCIA = 3          # 3 = ALICANTE
    OFICINA = 13           # 13 = OEX ALICANTE
    TRAMITE = 5            # 5 = POLICÍA - Solicitud Protección Temporal
    
    logger.info("Инициализирую браузер...")
    
    # Инициализируем браузер с undetected-chromedriver
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(START_URL, 5)
    
    try:
        # Создаём экземпляр класса NIESpecified
        nie_visa = NIESpecified(
            driver=driver,
            start_url=START_URL,
            passport=PASSPORT,
            full_name=NAME_SURNAME,
            birth_year=B_YEAR,
            provincia=PROVINCIA,
            oficina=OFICINA,
            tramite=TRAMITE
        )
        
        # Запускаем поиск цитаций
        nie_visa.search_for_citations()
        
    except KeyboardInterrupt:
        logger.info("\n\n⏹️ Поиск остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logger.critical(f"❌ Критическая ошибка: {type(e).__name__}: {e}")
    finally:
        logger.info("Закрываю браузер...")
        driver.quit()
        logger.info("✓ Браузер закрыт")


if __name__ == '__main__':
    main()
