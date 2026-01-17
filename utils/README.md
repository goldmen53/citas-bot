# Модуль Utils

Модуль утилит для CITAS Bot.

## Файлы

- `browser.py` - Инициализация браузера
- `wait.py` - Условия ожидания
- `block_handler.py` - Обработка блокировок
- `captcha.py` - Обработка капч
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
