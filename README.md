# 🎫 CITAS Bot - Автоматизированный поиск цитаций в Испании

Автоматизация для поиска цитаций в системе Офисов иностранцев Испании (НИЕ, ТИЕ и т.д.).

## 📋 Версии

- **v1.0** (ветка `v1.0-legacy`) - Первоначальная реализация для НИЕ с регионом
- **v2.0** (ветка `main`) - Модульная архитектура с поддержкой нескольких типов виз, Telegram Bot, Docker

## 🚀 Особенности v2.0

- ✅ **Поддержка нескольких виз**: НИЕ/ТИЕ, с/без региона
- ✅ **Telegram Bot**: Полный контроль через Telegram
- ✅ **Docker Compose**: Развёртывание с несколькими контейнерами
- ✅ **Ротация прокси**: Избежать блокировок по IP
- ✅ **Обработка капч**: Отправка пользователю через Telegram
- ✅ **База данных JSON**: Управление пользователями
- ✅ **Автоматическое извлечение**: Парсинг доступных цитаций
- ✅ **Логирование поисков**: История в БД

### 🎫 Поддерживаемые Типы Виз

| Тип | Статус | Описание |
|-----|--------|---------|
| **НИЕ с регионом** (visa_nie_spec) | ✅ РАБОТАЕТ | Поиск цитаций НИЕ с выбором провинции |
| **НИЕ национальный** (visa_nie_nat) | ⚠️ В РАЗРАБОТКЕ | Поиск НИЕ без региона - использует mock |
| **ТИЕ** (visa_tie) | ⚠️ В РАЗРАБОТКЕ | Поиск ТИЕ - использует mock |

📌 **Используй `visa_nie_spec`** для реального поиска цитаций!

## 📁 Структура проекта

```
citas-bot/
├── config/                    # Конфигурации
│   ├── visa_types.py         # Типы виз и маршруты
│   ├── app_config.py         # Общая конфигурация
│   └── proxies.json          # Список прокси
│
├── database/                 # Управление данными
│   ├── db_manager.py        # Менеджер БД JSON
│   ├── users.json           # База пользователей
│   └── search_history.json  # История поисков
│
├── modules/                 # Модули поиска
│   ├── base_visa.py        # Абстрактный базовый класс
│   ├── nie_specified.py    # НИЕ с регионом
│   ├── nie_national.py     # НИЕ без региона
│   ├── tie_specified.py    # ТИЕ с регионом
│   ├── tie_national.py     # ТИЕ без региона
│   ├── visa_factory.py     # Factory pattern
│   └── citation_extractor.py # Парсинг цитаций
│
├── telegram_bot/           # Бот Telegram
│   ├── bot_handler.py      # Основной обработчик
│   ├── commands/           # Доступные команды
│   │   ├── start.py
│   │   ├── register.py
│   │   ├── search.py
│   │   ├── status.py
│   │   ├── stop.py
│   │   └── help.py
│   └── callbacks/          # Обработчики callbacks
│       ├── captcha_handler.py
│       └── search_callbacks.py
│
├── utils/                  # Утилиты
│   ├── browser.py         # Инициализация Selenium
│   ├── wait.py            # Условия ожидания
│   ├── block_handler.py   # Обработка блокировок
│   ├── captcha.py         # Обработка капч
│   ├── logger.py          # Логирование
│   ├── proxy_manager.py   # Управление прокси
│   └── notifier.py        # Уведомления
│
├── containers/            # Docker
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
│
├── v1.0-legacy/          # Исходный код (архивирован)
├── .gitignore
├── .env.example
├── main.py               # Точка входа
└── README.md
```

## 🔧 Требования

- Python 3.10+
- Docker & Docker Compose
- Telegram Bot Token
- Прокси (опционально)

## 📦 Установка

### Локальная разработка

```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd citas-bot

# Создать venv
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Настроить .env
cp .env.example .env
# Отредактировать .env со своими данными
```

### Docker

```bash
docker-compose up -d
```

## 🤖 Использование с Telegram Bot

### Доступные команды

```
/start           - Запустить бот
/register        - Зарегистрировать нового пользователя
/search          - Начать поиск цитаций
/status          - Посмотреть статус поиска
/stop            - Остановить поиск
/help            - Справка
```

### Порядок использования

1. Запустите бот с `/start`
2. Зарегистрируйтесь с `/register` и следуйте инструкциям
3. Начните поиск с `/search`
4. Вы получите уведомление, когда найдутся цитации
5. Бот отправит вам капчи, если необходимо (решите в Telegram)

## 🗄️ Структура базы данных (JSON)

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

Автоматически запустятся:
- `telegram-bot`: Основной бот Telegram
- `worker-nie-spec-1`: Worker НИЕ с регионом (Прокси 1)
- `worker-nie-nat-1`: Worker НИЕ без региона (Прокси 2)
- Больше workers в зависимости от конфигурации

Каждый контейнер имеет свой прокси для избежания блокировок.

## 🔐 Переменные окружения

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_token_here

# Прокси (опционально)
PROXY_1=192.168.1.1:8080
PROXY_2=192.168.1.2:8080

# Логирование
LOG_LEVEL=INFO
```

## 📚 Ветки Git

- `main` - Главная ветка с модульной архитектурой (v2.0)
- `develop` - Ветка разработки
- `v1.0-legacy` - Исходный код (архивирован)
- `feature/*` - Ветки для features

## 🎓 Обучение

Этот проект - отличная возможность для обучения:

- ✅ Паттерны проектирования (Factory, Abstract Factory)
- ✅ Async/Await в Python
- ✅ Selenium & Web Scraping
- ✅ Telegram Bot API
- ✅ Docker & Docker Compose
- ✅ Управление прокси и anti-detection
- ✅ Логирование и отладка
- ✅ Профессиональный Git workflow

## ⚠️ Дисклеймер

Этот проект только в образовательных целях. Пользователь несёт ответственность за:
- Соблюдение условий обслуживания веб-сайта
- Местные и региональные законы
- Лимиты запросов и этичный веб-скрейпинг

## 📄 Лицензия

MIT

## 👤 Автор

Разработано для автоматизации поиска цитаций в Испании.

---

**Примечание**: Для версии v1.0 смотрите ветку `v1.0-legacy` или файл `citas-v1.0-backup.tar.gz`
