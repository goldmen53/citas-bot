# Модуль Telegram Bot

Бот Telegram для управления поиском цитаций.

## Структура

```
telegram_bot/
├── bot_handler.py      # Основной обработчик
├── commands/           # Команды
│   ├── start.py
│   ├── register.py
│   ├── search.py
│   ├── status.py
│   ├── stop.py
│   └── help.py
└── callbacks/          # Обработка callbacks
    ├── captcha_handler.py
    └── search_callbacks.py
```

## Использование

```python
from telegram_bot.bot_handler import CitasBot

bot = CitasBot(token="your_token")
bot.run()
```
