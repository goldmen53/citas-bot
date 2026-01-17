# Модуль Database

Модуль для управления базой данных JSON.

## Файлы

- `db_manager.py` - Менеджер БД JSON
- `users.json` - База пользователей
- `search_history.json` - История поисков

## Использование

```python
from database.db_manager import UserDatabase

db = UserDatabase()
user = db.get_user(telegram_id)
db.add_user(user_data)
```

## Структура данных

См. файлы JSON для полной структуры.
