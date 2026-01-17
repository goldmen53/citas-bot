# Config Module

Módulo de configuración para CITAS Bot.

## Archivos

- `visa_types.py` - Configuración de tipos de visa
- `app_config.py` - Configuración general de la aplicación
- `proxies.json` - Lista de proxys disponibles

## Uso

```python
from config.visa_types import VISA_CONFIGS
from config.app_config import settings

visa_config = VISA_CONFIGS['NIE_SPECIFIED']
timeout = settings.BROWSER_TIMEOUT
```
