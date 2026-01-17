# Utils

Módulo de utilidades para CITAS Bot.

## Archivos

- `browser.py` - Inicialización del navegador
- `wait.py` - Condiciones de espera
- `block_handler.py` - Manejo de bloqueos
- `captcha.py` - Manejo de captchas
- `logger.py` - Sistema de logging
- `proxy_manager.py` - Gestión de proxys
- `notifier.py` - Sistema de notificaciones

## Uso

```python
from utils.logger import setup_logger
from utils.proxy_manager import ProxyManager

logger = setup_logger(__name__)
proxy_manager = ProxyManager()
```
