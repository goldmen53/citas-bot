# Модуль Utils

Вспомогательные модули для работы с браузером и обработки данных.

## Файлы

### logger.py
Настройка логирования для всего проекта.
- `setup_logger(name, level)` - Создание логгера для модуля
- Логи сохраняются в `logs/citas.log`
- Цветной вывод в консоль + сохранение в файл

### wait.py
Функции для безопасного ожидания элементов на странице.
- `wait_clickable(driver, by, value, timeout)` - Ожидание кликабельного элемента
- `safe_wait_clickable(driver, by, value, timeout, default)` - Безопасное ожидание (без исключений)
- `wait_for_element(driver, by, value, timeout)` - Ожидание присутствия элемента в DOM

### block_handler.py
Обработка блокирующих состояний сайта.
- `guard_blocking_states(driver, start_url)` - Проверка 429, редиректов и блокировок
- `RestartLoop` - Исключение для перезагрузки цикла поиска
- `logger.py` - Система логирования
- `proxy_manager.py` - Управление прокси
- `notifier.py` - Система уведомлений

## Использование

```python
from utils.logger import setup_logger
from utils.proxy_manager import ProxyManager

logger = setup_logger(__name__)
proxy_manager = ProxyManager()
```
