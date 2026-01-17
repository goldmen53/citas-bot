# Git рабочий процесс для CITAS Bot

## Структура ветвей

```
main (v2.0 release branch)
  ├── develop (integration branch)
  │   ├── feature/modular-architecture (В РАЗРАБОТКЕ)
  │   ├── feature/telegram-integration
  │   ├── feature/docker-orchestration
  │   ├── feature/proxy-rotation
  │   └── feature/captcha-handling
  │
  └── v1.0-legacy (исходный код архивирован)
```

## Как работать

### 1. Создать новую функцию

```bash
# Из develop
git checkout develop
git pull origin develop

# Создать ветку функции
git checkout -b feature/название-функции

# Сделать изменения...
git add .
git commit -m "Feature: четкое описание"

# Отправить на сервер
git push origin feature/название-функции
```

### 2. Слияние в develop

```bash
git checkout develop
git merge --no-ff feature/название-функции
git push origin develop
```

### 3. Релиз на main (v2.0)

```bash
git checkout main
git merge --no-ff develop
git tag -a v2.0 -m "Release v2.0: Модульная архитектура с интеграцией Telegram"
git push origin main
git push origin v2.0
```

## Соглашения для commit'ов

Используйте формат: `Type: Описание`

- `feat:` - Новая функция
- `fix:` - Исправление ошибки
- `refactor:` - Изменения без изменения функциональности
- `docs:` - Изменения в документации
- `test:` - Добавление тестов
- `chore:` - Задачи техническое обслуживание

### Примеры

```bash
git commit -m "feat: Добавить модульную архитектуру виз"
git commit -m "fix: Исправить проблему с обработкой капчи"
git commit -m "docs: Обновить README с инструкцией Docker"
git commit -m "refactor: Извлечь общие обработчики Telegram"
```

## Текущая история

```
v1.0 (tag)
└── main: Добавить исходный код v1.0
    └── Initial commit: Конфигурация и документы
```

## Следующие шаги

1. `feature/modular-architecture` - Базовая структура
2. `feature/telegram-integration` - Бот Telegram
3. `feature/docker-orchestration` - Docker и прокси
4. Слияние в develop
5. Релиз v2.0 на main

## Восстановить v1.0 если нужно

```bash
# Просмотр кода v1.0
git checkout v1.0

# Или из любой ветки
git show v1.0:v1.0-legacy/CITA_NIE.py
```
