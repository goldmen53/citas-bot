# V1.0 Legacy Code

Este directorio contiene el código original (v1.0) de la implementación.

## Archivos

- `CITA_NIE.py` - Script principal para búsqueda de NIE con región
- `main.py` - Funciones auxiliares y utilidades
- `requirements.txt` - Dependencias del proyecto
- `Dockerfile` - Configuración Docker
- `docker-compose.yml` - Orquestación Docker
- `test.ipynb` - Notebook de pruebas

## Uso

Para usar el código legado:

```bash
cd v1.0-legacy/
python CITA_NIE.py
```

## Notas

Este código ha sido archivado como referencia. Para la versión nueva y mejorada, consulta la rama `feature/modular-architecture`.

### Limitaciones de v1.0

- ❌ Solo soporta NIE con región
- ❌ Sin interfaz Telegram
- ❌ Sin soporte múltiples usuarios
- ❌ Sin manejo de proxys automático
- ❌ Código monolítico sin modularización
- ❌ Notificaciones solo por sonido

### Mejoras en v2.0

- ✅ Múltiples tipos de visa
- ✅ Bot de Telegram completo
- ✅ Soporte para múltiples usuarios simultáneamente
- ✅ Rotación automática de proxys
- ✅ Arquitectura modular y escalable
- ✅ Notificaciones por Telegram
- ✅ Captura y manejo de captchas
