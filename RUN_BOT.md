#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# TELEGRAM BOT - ИНСТРУКЦИЯ ЗАПУСКА
# ═══════════════════════════════════════════════════════════════════════════════

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║              🚀 КАК ЗАПУСТИТЬ TELEGRAM БОТА (ИНСТРУКЦИЯ)                  ║
╚════════════════════════════════════════════════════════════════════════════╝

ТРЕБОВАНИЯ:
───────────────────────────────────────────────────────────────────────────────
✅ Python 3.10+
✅ Токен от @BotFather в Telegram (сохранён в .env)
✅ python-telegram-bot установлен
✅ Остальные зависимости установлены


ВАРИАНТ 1: ЗАПУСТИТЬ БОТА В КОНСОЛИ (для отладки)
───────────────────────────────────────────────────────────────────────────────

# Откройте терминал в корне проекта CITAS и выполните:

cd /home/yevhen/VScode/CITAS

# Убедитесь что .env файл содержит токен:
cat .env | grep TELEGRAM_BOT_TOKEN

# Установите зависимости (если ещё не установлены):
pip install -r requirements.txt

# Запустите бота:
PYTHONPATH=/home/yevhen/VScode/CITAS python3 telegram_bot/bot_handler.py

# Ожидаемый вывод:
# 2026-01-17 19:03:06 - telegram_bot - INFO - 🤖 Инициализация Telegram бота...
# 2026-01-17 19:03:06 - telegram_bot - INFO - ✅ Бот инициализирован успешно
# 2026-01-17 19:03:06 - telegram_bot - INFO - 🚀 Бот запущен на токене: 8575472682:A...
# 2026-01-17 19:03:06 - telegram_bot - INFO - ⏳ Ожидание входящих сообщений...

# Для остановки нажмите: Ctrl+C


ВАРИАНТ 2: ЗАПУСТИТЬ БОТА В ФОНЕ (для production)
───────────────────────────────────────────────────────────────────────────────

cd /home/yevhen/VScode/CITAS

# Запустить бота в фоне:
PYTHONPATH=/home/yevhen/VScode/CITAS nohup python3 telegram_bot/bot_handler.py > logs/telegram_bot.log 2>&1 &

# Проверить что бот запущен:
ps aux | grep bot_handler | grep -v grep

# Просмотреть логи:
tail -f logs/telegram_bot.log

# Остановить бота:
pkill -f bot_handler.py


ВАРИАНТ 3: ЗАПУСТИТЬ С СОХРАНЕНИЕМ В SYSTEMD (для Linux)
───────────────────────────────────────────────────────────────────────────────

# Создать systemd сервис (требуется sudo):
sudo tee /etc/systemd/system/citas-bot.service << 'SYSTEMD'
[Unit]
Description=CITAS Telegram Bot
After=network.target

[Service]
Type=simple
User=yevhen
WorkingDirectory=/home/yevhen/VScode/CITAS
Environment="PYTHONPATH=/home/yevhen/VScode/CITAS"
ExecStart=/usr/bin/python3 /home/yevhen/VScode/CITAS/telegram_bot/bot_handler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD

# Активировать сервис:
sudo systemctl daemon-reload
sudo systemctl enable citas-bot
sudo systemctl start citas-bot

# Проверить статус:
sudo systemctl status citas-bot

# Просмотреть логи:
sudo journalctl -u citas-bot -f


ВАРИАНТ 4: ТЕСТИРОВАТЬ БОТ (без запуска polling)
───────────────────────────────────────────────────────────────────────────────

cd /home/yevhen/VScode/CITAS

# Запустить тесты:
PYTHONPATH=/home/yevhen/VScode/CITAS python3 test_bot.py

# Результаты:
# ✅ PASSED     Инициализация БД
# ✅ PASSED     Регистрация пользователя
# ✅ PASSED     История поисков
# ✅ PASSED     Конфигурация .env
# ✅ PASSED     Импорт модулей
# ✅ PASSED     Инициализация бота
# ──────────────────────────────────────────────────────────────────────────
# Итого: 6/6 тестов пройдено
# ✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!


КОМАНДЫ БОТА
───────────────────────────────────────────────────────────────────────────────

После запуска бота откройте Telegram и напишите команду:

/start    - Запуск бота
/help     - Справка
/register - Регистрация (4 шага)
/search   - Поиск цитаций
/status   - Статус поиска
/stop     - Остановка поиска


ЛОГИ
───────────────────────────────────────────────────────────────────────────────

# Для консольного запуска - логи выводятся в консоль

# Для фонового запуска (nohup) - логи в файле:
tail -f logs/telegram_bot.log

# Для systemd:
sudo journalctl -u citas-bot -f

# Для основных логов:
tail -f logs/citas.log


ПРОБЛЕМЫ И РЕШЕНИЯ
───────────────────────────────────────────────────────────────────────────────

Проблема: "ModuleNotFoundError: No module named 'dotenv'"
Решение: pip install python-dotenv

Проблема: "ModuleNotFoundError: No module named 'telegram'"
Решение: pip install python-telegram-bot[all]

Проблема: "TELEGRAM_BOT_TOKEN не найден"
Решение: 
  1. Проверьте что .env файл в корне проекта
  2. Проверьте что в .env есть строка: TELEGRAM_BOT_TOKEN=...
  3. Проверьте что нет пробелов до/после токена

Проблема: Бот не отвечает на сообщения
Решение:
  1. Проверьте логи: tail -f logs/telegram_bot.log
  2. Проверьте интернет соединение
  3. Перезапустите бота

Проблема: "RuntimeError: This event loop is already running"
Решение: Это нормально при использовании timeout/nohup, бот всё равно запускается


БЫСТРЫЙ СТАРТ (скопируй и вставь)
───────────────────────────────────────────────────────────────────────────────

# Один коммит - бот запущен:

cd /home/yevhen/VScode/CITAS && \
PYTHONPATH=/home/yevhen/VScode/CITAS python3 telegram_bot/bot_handler.py


ПОЛЕЗНЫЕ КОМАНДЫ
───────────────────────────────────────────────────────────────────────────────

# Проверить что бот запущен:
ps aux | grep bot_handler | grep -v grep

# Остановить бота:
pkill -f bot_handler.py

# Посмотреть последние 50 строк логов:
tail -50 logs/telegram_bot.log

# Посмотреть ошибки в логах:
grep ERROR logs/telegram_bot.log

# Пересчитать строки логов:
wc -l logs/telegram_bot.log

# Запустить бота в фоне с выводом в консоль:
nohup python3 telegram_bot/bot_handler.py &


═══════════════════════════════════════════════════════════════════════════════

✅ БОТ ГОТОВ К ЗАПУСКУ!

Начните с вариант 1 (запуск в консоли) или выполните тесты (вариант 4).

═══════════════════════════════════════════════════════════════════════════════

EOF
