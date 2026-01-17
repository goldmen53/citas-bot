# Modules

Módulos para diferentes tipos de visa.

## Archivos

- `base_visa.py` - Clase base abstracta
- `nie_specified.py` - NIE con región
- `nie_national.py` - NIE sin región
- `tie_specified.py` - TIE con región
- `tie_national.py` - TIE sin región
- `visa_factory.py` - Factory para crear módulos
- `citation_extractor.py` - Extractor de citas

## Uso

```python
from modules.visa_factory import create_visa_bot

visa_bot = create_visa_bot(user_data)
visa_bot.run()
```
