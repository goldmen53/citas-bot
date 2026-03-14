"""
Базовый класс для всех типов виз.
Содержит общие методы для взаимодействия с веб-формами.
"""

import time
from random import randrange
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger import setup_logger
from utils.wait import wait_clickable, safe_wait_clickable
from utils.block_handler import guard_blocking_states, RestartLoop
from config.xpaths import get_xpaths

logger = setup_logger(__name__)


class BaseVisa(ABC):
    """
    Абстрактный базовый класс для всех типов виз.
    Предоставляет общие методы для работы с формами и элементами страницы.
    """
    
    def __init__(self, visa_type: str, driver, start_url: str):
        """
        Инициализация базового класса.
        
        Args:
            visa_type: Тип визы ('nie_specified', 'nie_national', 'tie')
            driver: Selenium WebDriver
            start_url: Исходный URL для перезагрузки при ошибках
        """
        self.visa_type = visa_type
        self.driver = driver
        self.start_url = start_url
        self.xpaths = get_xpaths(visa_type)
        logger.info(f"Инициализирован класс {self.__class__.__name__} (тип: {visa_type})")
    
    def click_button(self, actions, xpath: str, button_name: str = None, wait_time: float = 0.5):
        """
        Кликает по кнопке с использованием ActionChains.
        
        Args:
            actions: Selenium ActionChains объект
            xpath: XPath селектор кнопки
            button_name: Название кнопки для логирования
            wait_time: Время ожидания после клика (в секундах)
        
        Returns:
            False если успешно, True если нужно перезагрузить цикл
        """
        try:
            button_name = button_name or xpath
            logger.debug(f"Ищу кнопку: {button_name}")
            
            button = wait_clickable(self.driver, By.XPATH, xpath, timeout=10)
            logger.info(f"✓ Нажимаю кнопку: {button_name}")
            
            actions.move_to_element(button).click().perform()
            
            # Случайная задержка для anti-detection (как в v1.0)
            # После клика по кнопке используем случайную задержку вместо фиксированной
            delay = randrange(int(wait_time * 1000), int(wait_time * 2000)) / 1000.0
            time.sleep(delay if wait_time > 0.5 else wait_time)
            
            return False  # Успех
            
        except TimeoutException:
            logger.error(f"✗ Кнопка не найдена: {button_name}")
            raise RestartLoop(f"Кнопка {button_name} не найдена, перезагружаю цикл")
        
        except Exception as e:
            logger.error(f"⚠️ Ошибка при клике по кнопке {button_name}: {e}")
            raise RestartLoop(f"Ошибка при клике: {e}")
    
    def click_dropdown(self, actions, xpath: str, option_value, dropdown_name: str = None):
        """
        Выбирает опцию из выпадающего списка.
        
        Args:
            actions: Selenium ActionChains объект
            xpath: XPath селектор dropdown'а
            option_value: Значение или индекс опции для выбора
            dropdown_name: Название dropdown'а для логирования
        
        Returns:
            False если успешно, True если нужно перезагрузить цикл
        """
        try:
            dropdown_name = dropdown_name or xpath
            logger.debug(f"Открываю dropdown: {dropdown_name}")
            
            dropdown_element = wait_clickable(self.driver, By.XPATH, xpath, timeout=10)
            select = Select(dropdown_element)
            
            # Выбор по индексу или по значению
            if isinstance(option_value, int):
                logger.info(f"✓ Выбираю опцию {option_value} в {dropdown_name}")
                select.select_by_index(option_value)
            else:
                logger.info(f"✓ Выбираю опцию '{option_value}' в {dropdown_name}")
                select.select_by_value(str(option_value))
            
            time.sleep(0.3)
            return False  # Успех
            
        except TimeoutException:
            logger.error(f"✗ Dropdown не найден: {dropdown_name}")
            raise RestartLoop(f"Dropdown {dropdown_name} не найден")
        
        except NoSuchElementException:
            logger.error(f"✗ Опция {option_value} не найдена в {dropdown_name}")
            raise RestartLoop(f"Опция не найдена в {dropdown_name}")
        
        except Exception as e:
            logger.error(f"⚠️ Ошибка при выборе из dropdown {dropdown_name}: {e}")
            raise RestartLoop(f"Ошибка в dropdown: {e}")
    
    def enter_text(self, actions, xpath: str, text: str, field_name: str = None):
        """
        Вводит текст в текстовое поле.
        
        Args:
            actions: Selenium ActionChains объект
            xpath: XPath селектор поля ввода
            text: Текст для ввода
            field_name: Название поля для логирования
        
        Returns:
            False если успешно, True если нужно перезагрузить цикл
        """
        try:
            field_name = field_name or xpath
            logger.debug(f"Заполняю поле: {field_name}")
            
            input_element = wait_clickable(self.driver, By.XPATH, xpath, timeout=10)
            
            # Очищаем поле
            input_element.clear()
            
            # Вводим текст с паузами для anti-detection
            # Имитируем медленный ввод как человек
            for char in text:
                input_element.send_keys(char)
                # Случайная пауза между символами (20-100 мс)
                time.sleep(randrange(20, 100) / 1000.0)
            
            logger.info(f"✓ В поле '{field_name}' введено: {text[:20]}..." if len(text) > 20 else f"✓ В поле '{field_name}' введено: {text}")
            
            # Пауза после завершения ввода
            time.sleep(randrange(100, 300) / 1000.0)
            return False  # Успех
            
        except TimeoutException:
            logger.error(f"✗ Поле не найдено: {field_name}")
            raise RestartLoop(f"Поле {field_name} не найдено")
        
        except Exception as e:
            logger.error(f"⚠️ Ошибка при заполнении поля {field_name}: {e}")
            raise RestartLoop(f"Ошибка при вводе текста: {e}")
    
    def check_blocking_states(self) -> bool:
        """
        Проверяет блокирующие состояния сайта.
        
        Returns:
            True если обнаружено блокирующее состояние
            False если всё в порядке
        """
        return guard_blocking_states(self.driver, self.start_url)
    
    @abstractmethod
    def search_for_citations(self):
        """
        Основной метод поиска цитат.
        Должен быть реализован в подклассах.
        """
        pass
