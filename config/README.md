# Модуль Config

Модуль конфигурации для CITAS Bot.

## Файлы

- `visa_types.py` - Конфигурация типов виз
- `app_config.py` - Общая конфигурация приложения
- `proxies.json` - Список доступных прокси

## Использование

```python
from config.visa_types import VISA_CONFIGS
from config.app_config import settings

visa_config = VISA_CONFIGS['NIE_SPECIFIED']
timeout = settings.BROWSER_TIMEOUT
```
