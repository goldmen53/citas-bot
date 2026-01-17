# Модуль Config

Центральное хранилище конфигураций для CITAS Bot.

## Файлы

### xpaths.py
XPath'ы и селекторы для всех типов виз.
- `XPATHS` - Словарь с XPath'ами для каждого типа визы
- `get_xpaths(visa_type)` - Функция получения XPath'ов для конкретного типа

Структура:
```
XPATHS = {
    'common': {...},           # Общие элементы для всех виз
    'nie_specified': {...},    # НИЕ с регионом
    'nie_national': {...},     # НИЕ национальный
    'tie': {...},              # ТИЕ
}
```

### visa_types.py (будет создан)
Конфигурация параметров для каждого типа визы.

### app_config.py (будет создан)
Общие параметры приложения (таймауты, количество попыток, задержки и т.д.).

### proxies.json (будет создан)
Список доступных прокси-серверов для ротации.

## Использование

```python
from config.xpaths import get_xpaths
from config.visa_types import VISA_CONFIGS
from config.app_config import settings

# Получить XPath'ы для конкретной визы
xpaths = get_xpaths('nie_specified')
button_xpath = xpaths['accept_button']

# Получить конфигурацию визы
visa_config = VISA_CONFIGS['NIE_SPECIFIED']

# Получить параметры приложения
timeout = settings.BROWSER_TIMEOUT
```
