# Database Module

Módulo para gestión de base de datos JSON.

## Archivos

- `db_manager.py` - Gestor principal de BD
- `users.json` - Base de datos de usuarios
- `search_history.json` - Historial de búsquedas

## Uso

```python
from database.db_manager import UserDatabase

db = UserDatabase()
user = db.get_user(telegram_id)
db.add_user(user_data)
```

## Estructura de Datos

Ver archivos JSON para estructura completa.
