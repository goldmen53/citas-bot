"""
ИНСТРУКЦИЯ: Как создать Telegram бота

Этот файл содержит пошаговую инструкцию по созданию Telegram бота.
Следуйте этим шагам, чтобы получить TOKEN для вашего бота.
"""

# 📱 ПОШАГОВАЯ ИНСТРУКЦИЯ ПО СОЗДАНИЮ TELEGRAM БОТА

# ═══════════════════════════════════════════════════════════════════════════════

# ШАГИ:

# 1️⃣  ОТКРОЙТЕ TELEGRAM

#     Скачайте Telegram на свой телефон:
#     • iOS: App Store
#     • Android: Google Play
#     • Или используйте веб-версию: https://web.telegram.org

# ═══════════════════════════════════════════════════════════════════════════════

# 2️⃣  НАЙДИТЕ @BotFather

#     Откройте поиск в Telegram (значок лупы)
#     Введите: @BotFather
#     (Это официальный бот Telegram для создания ботов)

# ═══════════════════════════════════════════════════════════════════════════════

# 3️⃣  НАПИШИТЕ /newbot

#     Откройте чат с @BotFather
#     Напишите: /newbot
#     Нажмите Send

#     BotFather ответит:
#     "Alright, a new bot. How are we going to call it?
#      Please choose a name for your bot."

# ═══════════════════════════════════════════════════════════════════════════════

# 4️⃣  ВВЕДИТЕ ИМЯ БОТА

#     BotFather попросит два имени:
#     
#     a) Displayable Name (видимое имя):
#        Напишите: CITAS Bot
#        (Это то имя, которое видят пользователи)
#     
#     b) Username (уникальное имя для @):
#        Напишите: citas_citations_bot
#        (или любое другое уникальное имя без пробелов, только буквы, цифры, подчёркивание)
#        Имя должно заканчиваться на _bot
#
#     Пример:
#        your_project_bot
#        citation_finder_bot
#        citas_automation_bot

# ═══════════════════════════════════════════════════════════════════════════════

# 5️⃣  ПОЛУЧИТЕ TOKEN

#     После того как вы ввели имя, BotFather ответит:
#
#     "Done! Congratulations on your new bot.
#      You will find it at t.me/citas_citations_bot
#      You can now add a description, about section,
#      and commands for your bot. Use the /setcommands command to change them.
#      
#      Here's your token, keep it safe and secure:
#      
#      1234567890:ABCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhI"

#     ⚠️  ВАЖНО: СКОПИРУЙТЕ ЭТОТ TOKEN!
#         Это уникальный ключ для вашего бота.
#         Никому его не показывайте!

# ═══════════════════════════════════════════════════════════════════════════════

# 6️⃣  СОХРАНИТЕ TOKEN В .env ФАЙЛЕ

#     Откройте файл .env в проекте:
#     
#     .env
#     ────────────────────────────────────
#     TELEGRAM_BOT_TOKEN=1234567890:ABCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhI
#     TELEGRAM_CHAT_ID=YOUR_CHAT_ID
#     ────────────────────────────────────
#
#     Замените 1234567890:ABCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhI на ваш токен!

# ═══════════════════════════════════════════════════════════════════════════════

# 7️⃣  УСТАНОВИТЕ КОМАНДЫ

#     Напишите @BotFather: /setcommands
#     
#     BotFather ответит: "Which bot would you like to configure?"
#     Выберите вашего бота из списка (например, @citas_citations_bot)
#     
#     Затем скопируйте этот текст и отправьте его:
#
#     start - Запустить бота
#     register - Зарегистрировать нового пользователя
#     search - Начать поиск цитаций
#     status - Посмотреть статус поиска
#     stop - Остановить поиск
#     help - Справка и помощь

# ═══════════════════════════════════════════════════════════════════════════════

# 8️⃣  ПОЛУЧИТЕ СВОЙ CHAT_ID (для тестирования)

#     Напишите боту: /start
#     
#     Затем откройте ссылку в браузере:
#     https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#     
#     Замените <YOUR_TOKEN> на ваш токен
#     
#     Пример:
#     https://api.telegram.org/bot1234567890:ABCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhI/getUpdates
#     
#     Вы увидите JSON ответ:
#     {
#       "ok": true,
#       "result": [
#         {
#           "update_id": 123456789,
#           "message": {
#             "message_id": 1,
#             "from": {
#               "id": 1234567890,  ← ЭТО ВАШ CHAT_ID
#               "is_bot": false,
#               "first_name": "Your Name"
#             },
#             ...
#           }
#         }
#       ]
#     }
#     
#     Скопируйте "id" и сохраните в .env:
#     TELEGRAM_CHAT_ID=1234567890

# ═══════════════════════════════════════════════════════════════════════════════

# 9️⃣  ГОТОВО!

#     Теперь у вас есть:
#     ✅ TELEGRAM_BOT_TOKEN - для управления ботом
#     ✅ TELEGRAM_CHAT_ID - для отправки сообщений вам
#     ✅ Команды зарегистрированы в @BotFather
#     ✅ Бот готов к использованию

# ═══════════════════════════════════════════════════════════════════════════════

# 📝 ПРИМЕРЫ ТОКЕНОВ (ФЕЙК - НЕ ИСПОЛЬЗУЙТЕ):

# Это просто примеры формата, реальные токены выглядят так:
# 1234567890:ABCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhI
# 987654321:XyZaBcDeFgHiJkLmNoPqRsT

# ═══════════════════════════════════════════════════════════════════════════════

# 🔒 БЕЗОПАСНОСТЬ:

# ⚠️  НИКОГДА не делитесь своим токеном!
# ⚠️  НИКОГДА не коммитьте токен в Git!
# ⚠️  ИСПОЛЬЗУЙТЕ .env файл для хранения токена
# ⚠️  ДОБАВЬТЕ .env в .gitignore

# ═══════════════════════════════════════════════════════════════════════════════

# 💡 ПОЛЕЗНЫЕ ССЫЛКИ:

# • Telegram Bot API: https://core.telegram.org/bots/api
# • BotFather: https://t.me/botfather
# • python-telegram-bot: https://python-telegram-bot.readthedocs.io/
# • Примеры ботов: https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

# ═══════════════════════════════════════════════════════════════════════════════

# 🎓 ПОСЛЕ СОЗДАНИЯ БОТА:

# 1. Сохраните токен в .env
# 2. Запустите бота: python3 telegram_bot/bot_handler.py
# 3. Откройте t.me/YOUR_BOT_NAME в Telegram
# 4. Напишите /start для тестирования

# ═══════════════════════════════════════════════════════════════════════════════
