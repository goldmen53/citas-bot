# Модуль Modules

Модули для различных типов виз.

## Файлы

- `base_visa.py` - Абстрактный базовый класс
- `nie_specified.py` - НИЕ с регионом
- `nie_national.py` - НИЕ без региона
- `tie_specified.py` - ТИЕ с регионом
- `tie_national.py` - ТИЕ без региона
- `visa_factory.py` - Factory для создания модулей
- `citation_extractor.py` - Парсер цитаций

## Использование

```python
from modules.visa_factory import create_visa_bot

visa_bot = create_visa_bot(user_data)
visa_bot.run()
```
