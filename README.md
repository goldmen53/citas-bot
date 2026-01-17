# 🎫 CITAS Bot - Búsqueda Automatizada de Citas en España

Automatización para búsqueda de citas en el sistema de Oficinas de Extranjería de España (NIE, TIE, etc).

## 📋 Versiones

- **v1.0** (rama `v1.0-legacy`) - Implementación inicial para NIE con región
- **v2.0** (rama `main`) - Arquitectura modular con soporte para múltiples tipos de visa, Telegram Bot, Docker

## 🚀 Características v2.0

- ✅ **Soporte múltiples visas**: NIE/TIE, con/sin región
- ✅ **Telegram Bot**: Control completo vía Telegram
- ✅ **Docker Compose**: Despliegue con múltiples contenedores
- ✅ **Rotación de Proxys**: Evitar bloqueos por IP
- ✅ **Manejo de Captchas**: Envío a usuario vía Telegram
- ✅ **Base de Datos JSON**: Gestión de usuarios
- ✅ **Extracción automática**: Parsingde citas disponibles
- ✅ **Registro de búsquedas**: Historial en BD

## 📁 Estructura del Proyecto

```
citas-bot/
├── config/                    # Configuraciones
│   ├── visa_types.py         # Tipos de visa y rutas
│   ├── app_config.py         # Configuración general
│   └── proxies.json          # Lista de proxys
│
├── database/                 # Gestión de datos
│   ├── db_manager.py        # Gestor de BD JSON
│   ├── users.json           # Base de usuarios
│   └── search_history.json  # Historial de búsquedas
│
├── modules/                 # Módulos de búsqueda
│   ├── base_visa.py        # Clase base abstracta
│   ├── nie_specified.py    # NIE con región
│   ├── nie_national.py     # NIE sin región
│   ├── tie_specified.py    # TIE con región
│   ├── tie_national.py     # TIE sin región
│   ├── visa_factory.py     # Factory pattern
│   └── citation_extractor.py # Parsing de citas
│
├── telegram_bot/           # Bot de Telegram
│   ├── bot_handler.py      # Manejador principal
│   ├── commands/           # Comandos disponibles
│   │   ├── start.py
│   │   ├── register.py
│   │   ├── search.py
│   │   ├── status.py
│   │   ├── stop.py
│   │   └── help.py
│   └── callbacks/          # Manejadores de callbacks
│       ├── captcha_handler.py
│       └── search_callbacks.py
│
├── utils/                  # Utilidades
│   ├── browser.py         # Inicialización Selenium
│   ├── wait.py            # Wait conditions
│   ├── block_handler.py   # Manejo de bloqueos
│   ├── captcha.py         # Handling de captchas
│   ├── logger.py          # Logging
│   ├── proxy_manager.py   # Gestión de proxys
│   └── notifier.py        # Notificaciones
│
├── containers/            # Docker
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
│
├── v1.0-legacy/          # Código original (archivado)
├── .gitignore
├── .env.example
├── main.py               # Punto de entrada
└── README.md
```

## 🔧 Requisitos

- Python 3.10+
- Docker & Docker Compose
- Telegram Bot Token
- Proxys (opcional)

## 📦 Instalación

### Desarrollo Local

```bash
# Clonar repositorio
git clone <your-repo-url>
cd citas-bot

# Crear venv
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus datos
```

### Docker

```bash
docker-compose up -d
```

## 🤖 Uso con Telegram Bot

### Comandos disponibles

```
/start           - Iniciar bot
/register        - Registrar nuevo usuario
/search          - Iniciar búsqueda de citas
/status          - Ver estado de búsqueda
/stop            - Detener búsqueda
/help            - Ayuda
```

### Flujo de uso

1. Inicia el bot con `/start`
2. Registrate con `/register` y sigue los pasos
3. Inicia búsqueda con `/search`
4. Recibirás notificación cuando se encuentren citas
5. El bot te enviará captchas si es necesario (resuelve en Telegram)

## 🗄️ Estructura de Base de Datos (JSON)

### users.json
```json
{
  "users": [
    {
      "telegram_id": "123456789",
      "name": "John Doe",
      "visa_type": "NIE_SPECIFIED",
      "passport": "ABC123456",
      "birth_year": "1990",
      "provincia": 3,
      "oficina": 13,
      "tramite": 5,
      "search_active": false,
      "created_at": "2025-01-17T10:00:00",
      "last_search": "2025-01-17T15:30:00"
    }
  ]
}
```

## 🐳 Docker Compose

Se levantarán automáticamente:
- `telegram-bot`: Bot principal de Telegram
- `worker-nie-spec-1`: Worker NIE con región (Proxy 1)
- `worker-nie-nat-1`: Worker NIE sin región (Proxy 2)
- Más workers según configuración

Cada container tiene su propia proxy para evitar bloqueos.

## 🔐 Variables de Entorno

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_token_here

# Proxys (opcional)
PROXY_1=192.168.1.1:8080
PROXY_2=192.168.1.2:8080

# Logging
LOG_LEVEL=INFO
```

## 📚 Ramas Git

- `main` - Rama principal con arquitectura modular (v2.0)
- `develop` - Rama de desarrollo
- `v1.0-legacy` - Código original (archivado)
- `feature/*` - Ramas de features

## 🎓 Aprendizaje

Este proyecto es una excelente oportunidad para aprender:

- ✅ Patrones de diseño (Factory, Abstract Factory)
- ✅ Async/Await en Python
- ✅ Selenium & Web Scraping
- ✅ Telegram Bot API
- ✅ Docker & Docker Compose
- ✅ Gestión de prox y anti-detection
- ✅ Logging y debugging
- ✅ Git workflow profesional

## ⚠️ Disclaimer

Este proyecto es solo con fines educativos. El usuario es responsable del cumplimiento de:
- Términos de servicio del sitio web
- Leyes locales y regionales
- Límite de solicitudes y manejo ético del web scraping

## 📄 Licencia

MIT

## 👤 Autor

Desarrollado para automatización de búsqueda de citas en España.

---

**Nota**: Para versión anterior (v1.0), consulta la rama `v1.0-legacy` o archivo `citas-v1.0-backup.tar.gz`
