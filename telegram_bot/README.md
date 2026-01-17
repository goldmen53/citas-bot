# Telegram Bot

Bot de Telegram para gestionar búsquedas de citas.

## Estructura

```
telegram_bot/
├── bot_handler.py      # Manejador principal
├── commands/           # Comandos
│   ├── start.py
│   ├── register.py
│   ├── search.py
│   ├── status.py
│   ├── stop.py
│   └── help.py
└── callbacks/          # Manejo de callbacks
    ├── captcha_handler.py
    └── search_callbacks.py
```

## Uso

```python
from telegram_bot.bot_handler import CitasBot

bot = CitasBot(token="your_token")
bot.run()
```
