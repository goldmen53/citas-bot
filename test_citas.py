"""
Модульные тесты для проекта CITAS.

Содержит unit тесты для всех основных компонентов:
- logger, wait, block_handler, config, base_visa, nie_specified
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Добавим корневую директорию в PATH
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from utils.wait import wait_clickable, safe_wait_clickable, wait_for_element
from utils.block_handler import guard_blocking_states, RestartLoop
from config.xpaths import get_xpaths, XPATHS
from modules.base_visa import BaseVisa
from modules.nie_specified import NIESpecified


class TestLogger(unittest.TestCase):
    """Тесты для модуля логирования."""
    
    def test_logger_creation(self):
        """Тест создания логгера."""
        logger = setup_logger('test_logger')
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'test_logger')
    
    def test_logger_has_handlers(self):
        """Тест что логгер имеет обработчики."""
        logger = setup_logger('test_logger')
        self.assertGreater(len(logger.handlers), 0)
    
    def test_logger_logging(self):
        """Тест логирования сообщений."""
        logger = setup_logger('test_logger')
        try:
            logger.info("Test message")
            logger.warning("Warning message")
            logger.error("Error message")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Логирование вызвало исключение: {e}")


class TestXPathConfig(unittest.TestCase):
    """Тесты для конфигурации XPath'ов."""
    
    def test_xpaths_structure(self):
        """Тест структуры XPATHS словаря."""
        self.assertIn('common', XPATHS)
        self.assertIn('nie_specified', XPATHS)
        self.assertIn('nie_national', XPATHS)
    
    def test_get_xpaths_nie_specified(self):
        """Тест получения XPath'ов для NIE specified."""
        xpaths = get_xpaths('nie_specified')
        self.assertIsInstance(xpaths, dict)
        self.assertGreater(len(xpaths), 0)
        # Должны быть как специфичные, так и общие XPath'ы
        self.assertIn('form', xpaths)  # nie_specified специфичный
        self.assertIn('cookie_close', xpaths)  # common
    
    def test_get_xpaths_nie_national(self):
        """Тест получения XPath'ов для NIE national."""
        xpaths = get_xpaths('nie_national')
        self.assertIsInstance(xpaths, dict)
        self.assertGreater(len(xpaths), 0)
    
    def test_xpaths_values_are_strings(self):
        """Тест что все XPath'ы - строки."""
        xpaths = get_xpaths('nie_specified')
        for key, value in xpaths.items():
            self.assertIsInstance(value, str, f"XPath '{key}' должен быть строкой")


class TestBlockHandler(unittest.TestCase):
    """Тесты для обработчика блокировок."""
    
    def test_restart_loop_exception(self):
        """Тест исключения RestartLoop."""
        with self.assertRaises(RestartLoop):
            raise RestartLoop("Test message")
    
    def test_guard_blocking_states_with_mock(self):
        """Тест guard_blocking_states с mock драйвером."""
        # Создаём mock драйвера
        mock_driver = MagicMock()
        mock_driver.page_source = "normal content"
        # Mock для find_element - нет "Go Back" кнопки
        mock_driver.find_element.side_effect = Exception("NoSuchElementException")
        
        # Должно вернуть False (нет блокировки)
        result = guard_blocking_states(mock_driver, 'http://example.com')
        self.assertFalse(result)
    
    def test_guard_blocking_states_429(self):
        """Тест обнаружения 429 ошибки."""
        mock_driver = MagicMock()
        mock_driver.page_source = "429 Too Many Requests"
        
        # Должно вернуть True (обнаружена блокировка)
        result = guard_blocking_states(mock_driver, 'http://example.com')
        self.assertTrue(result)


class TestBaseVisa(unittest.TestCase):
    """Тесты для абстрактного класса BaseVisa."""
    
    def setUp(self):
        """Подготовка к тестам."""
        self.mock_driver = MagicMock()
        self.start_url = 'http://example.com'
    
    def test_base_visa_initialization(self):
        """Тест инициализации BaseVisa."""
        # BaseVisa абстрактный, поэтому мы используем NIESpecified
        nie = NIESpecified(
            driver=self.mock_driver,
            start_url=self.start_url,
            passport='TEST123',
            full_name='Test Name',
            birth_year='1990',
            provincia=1,
            oficina=1,
            tramite=1
        )
        
        self.assertEqual(nie.visa_type, 'nie_specified')
        self.assertEqual(nie.start_url, self.start_url)
        self.assertEqual(nie.passport, 'TEST123')
    
    def test_base_visa_has_required_methods(self):
        """Тест что BaseVisa имеет необходимые методы."""
        nie = NIESpecified(
            driver=self.mock_driver,
            start_url=self.start_url,
            passport='TEST123',
            full_name='Test Name',
            birth_year='1990',
            provincia=1,
            oficina=1,
            tramite=1
        )
        
        required_methods = [
            'click_button',
            'click_dropdown',
            'enter_text',
            'check_blocking_states',
            'search_for_citations'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(nie, method_name),
                f"Метод {method_name} не найден в NIESpecified"
            )


class TestNIESpecified(unittest.TestCase):
    """Тесты для класса NIESpecified."""
    
    def setUp(self):
        """Подготовка к тестам."""
        self.mock_driver = MagicMock()
        self.start_url = 'http://example.com'
        self.nie = NIESpecified(
            driver=self.mock_driver,
            start_url=self.start_url,
            passport='FV315480',
            full_name='Yevhen Maksymov',
            birth_year='1991',
            provincia=3,
            oficina=13,
            tramite=5
        )
    
    def test_nie_specified_initialization(self):
        """Тест инициализации NIESpecified."""
        self.assertEqual(self.nie.passport, 'FV315480')
        self.assertEqual(self.nie.full_name, 'Yevhen Maksymov')
        self.assertEqual(self.nie.birth_year, '1991')
        self.assertEqual(self.nie.provincia, 3)
        self.assertEqual(self.nie.oficina, 13)
        self.assertEqual(self.nie.tramite, 5)
    
    def test_nie_specified_has_specialized_methods(self):
        """Тест что NIESpecified имеет специализированные методы."""
        specialized_methods = [
            'close_cookie_popup',
            'select_provincia_and_accept',
            'select_oficina_and_tramite',
            'enter_person_data',
            'submit_form',
            'check_citations_available',
            'handle_citations_found',
            'exit_and_restart'
        ]
        
        for method_name in specialized_methods:
            self.assertTrue(
                hasattr(self.nie, method_name),
                f"Метод {method_name} не найден"
            )
            self.assertTrue(
                callable(getattr(self.nie, method_name)),
                f"{method_name} не является методом"
            )
    
    def test_nie_specified_xpaths_loaded(self):
        """Тест что XPath'ы загружены."""
        self.assertIsNotNone(self.nie.xpaths)
        self.assertGreater(len(self.nie.xpaths), 0)
    
    def test_nie_specified_counter_initialization(self):
        """Тест инициализации счётчика попыток."""
        self.assertEqual(self.nie.attempt_counter, 0)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты для взаимодействия модулей."""
    
    def test_modules_import_chain(self):
        """Тест цепочки импортов модулей."""
        # Это тест что все импорты работают вместе
        from modules.nie_specified import NIESpecified
        from modules.base_visa import BaseVisa
        from utils.logger import setup_logger
        from config.xpaths import get_xpaths
        
        # Все импорты успешны
        self.assertTrue(True)
    
    def test_nie_specified_with_xpaths(self):
        """Тест NIESpecified с реальными XPath'ами."""
        mock_driver = MagicMock()
        nie = NIESpecified(
            driver=mock_driver,
            start_url='http://example.com',
            passport='TEST',
            full_name='Test User',
            birth_year='1990',
            provincia=1,
            oficina=1,
            tramite=1
        )
        
        # Проверим что XPath'ы загружены
        self.assertIn('form', nie.xpaths)
        self.assertIn('accept_button', nie.xpaths)
        self.assertIn('passport_input', nie.xpaths)


class TestLogging(unittest.TestCase):
    """Тесты логирования."""
    
    def test_log_file_exists(self):
        """Тест что лог файл создается."""
        logger = setup_logger('test_logging')
        logger.info("Test message for log file")
        
        log_path = Path('logs/citas.log')
        self.assertTrue(log_path.exists(), "Лог файл не создан")
    
    def test_log_file_contains_message(self):
        """Тест что сообщение записано в лог файл."""
        test_message = "UNIQUE_TEST_MESSAGE_12345"
        logger = setup_logger('test_unique')
        logger.info(test_message)
        
        log_path = Path('logs/citas.log')
        with open(log_path, 'r') as f:
            content = f.read()
            self.assertIn(test_message, content)


def run_tests():
    """Запуск всех тестов."""
    # Создаём test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestXPathConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestBaseVisa))
    suite.addTests(loader.loadTestsFromTestCase(TestNIESpecified))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestLogging))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Выводим итоговый отчёт
    print("\n" + "="*70)
    print(f"Всего тестов запущено: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Ошибки: {len(result.errors)}")
    print(f"Сбои: {len(result.failures)}")
    print("="*70)
    
    # Выход с правильным кодом
    sys.exit(0 if result.wasSuccessful() else 1)
