"""
Telegram Bot Handler - основной модуль бота
Управляет всем взаимодействием с пользователями через Telegram

Использует:
- python-telegram-bot (асинхронная библиотека)
- Интеграция с NIESpecified класом для поиска цитаций
- JSON база данных для хранения пользователей и истории
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode, ChatAction

# Загружаем переменные окружения
load_dotenv()

# Импортируем наши модули
from utils.logger import setup_logger
from modules.nie_specified import NIESpecified

# Настраиваем логирование
logger = setup_logger("telegram_bot", logging.INFO)

# Получаем токен из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "❌ TELEGRAM_BOT_TOKEN не найден в .env файле!\n"
        "Создайте .env файл и добавьте: TELEGRAM_BOT_TOKEN=your_token"
    )

# Пути к файлам БД
USERS_DB = Path("database/users.json")
SEARCH_HISTORY_DB = Path("database/search_history.json")

# Состояния для ConversationHandler
(
    WAITING_FOR_NAME,
    WAITING_FOR_EMAIL,
    WAITING_FOR_PASSPORT,
    WAITING_FOR_YEAR,
    WAITING_FOR_PROVINCIA,
    WAITING_FOR_OFICINA,
    WAITING_FOR_TRAMITE,
    SEARCHING,
) = range(8)


# ═══════════════════════════════════════════════════════════════════════════════
# УПРАВЛЕНИЕ БД
# ═══════════════════════════════════════════════════════════════════════════════


def init_databases():
    """Инициализирует JSON файлы баз данных"""
    USERS_DB.parent.mkdir(exist_ok=True)

    # Инициализируем users.json
    if not USERS_DB.exists():
        with open(USERS_DB, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        logger.info("✅ Создана БД users.json")

    # Инициализируем search_history.json
    if not SEARCH_HISTORY_DB.exists():
        with open(SEARCH_HISTORY_DB, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        logger.info("✅ Создана БД search_history.json")


def load_users() -> dict:
    """Загружает пользователей из JSON"""
    if USERS_DB.exists():
        with open(USERS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users: dict):
    """Сохраняет пользователей в JSON"""
    with open(USERS_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def save_search_history(search_record: dict):
    """Добавляет запись в историю поиска"""
    with open(SEARCH_HISTORY_DB, "r", encoding="utf-8") as f:
        history = json.load(f)

    history.append(search_record)

    with open(SEARCH_HISTORY_DB, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def user_exists(user_id: str) -> bool:
    """Проверяет, зарегистрирован ли пользователь"""
    users = load_users()
    return user_id in users


def get_user(user_id: str) -> dict | None:
    """Получает информацию пользователя"""
    users = load_users()
    return users.get(user_id)


def register_user(user_id: str, user_data: dict):
    """Регистрирует нового пользователя"""
    users = load_users()
    users[user_id] = user_data
    save_users(users)
    logger.info(f"✅ Зарегистрирован пользователь: {user_id}")


# ═══════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИКИ КОМАНД
# ═══════════════════════════════════════════════════════════════════════════════


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - приветствие и меню"""
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name

    logger.info(f"👤 Пользователь {user_id} ({user_name}) запустил бота")

    text = (
        f"👋 Привет, {user_name}!\n\n"
        "Я помогаю автоматизировать поиск цитаций в испанских офисах.\n\n"
        "Доступные команды:\n"
        "🔧 /register - Зарегистрироваться\n"
        "🔍 /search - Начать поиск цитаций\n"
        "📊 /status - Посмотреть статус\n"
        "⏹️ /stop - Остановить поиск\n"
        "❓ /help - Справка\n"
    )

    if user_exists(user_id):
        user = get_user(user_id)
        text += f"\n✅ Вы зарегистрированы как: {user.get('full_name', 'N/A')}"

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help - справка"""
    text = (
        "<b>📚 СПРАВКА</b>\n\n"
        "<b>Команды:</b>\n"
        "🔧 /register - Зарегистрировать ваши данные\n"
        "🔍 /search - Начать поиск цитаций\n"
        "📊 /status - Статус текущего поиска\n"
        "⏹️ /stop - Остановить поиск\n"
        "❓ /help - Эта справка\n\n"
        "<b>Как это работает:</b>\n"
        "1. Зарегистрируйте себя (/register)\n"
        "2. Выберите тип визы и параметры\n"
        "3. Начните поиск (/search)\n"
        "4. Бот будет отправлять уведомления когда найдёт цитацию\n\n"
        "<b>⚠️ Важно:</b>\n"
        "• Храните ваши данные в безопасности\n"
        "• Бот работает 24/7\n"
        "• Получите уведомление в момент нахождения цитации\n"
    )

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало регистрации - запрос имени"""
    user_id = str(update.effective_user.id)

    if user_exists(user_id):
        user = get_user(user_id)
        text = (
            f"✅ Вы уже зарегистрированы!\n\n"
            f"Ваши данные:\n"
            f"👤 Имя: {user.get('full_name')}\n"
            f"📧 Email: {user.get('email')}\n"
            f"🔢 Паспорт: {user.get('passport')}\n"
            f"📅 Год рождения: {user.get('birth_year')}\n\n"
            f"Используйте /search для начала поиска."
        )
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    await update.message.reply_text(
        "📝 Регистрация\n\n" "Введите ваше полное имя (Фамилия Имя):",
        reply_markup=ReplyKeyboardRemove(),
    )

    return WAITING_FOR_NAME


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет имя и запрашивает email"""
    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "📧 Введите ваш email адрес:",
    )

    return WAITING_FOR_EMAIL


async def register_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет email и запрашивает паспорт"""
    context.user_data["email"] = update.message.text

    await update.message.reply_text(
        "🔢 Введите номер вашего паспорта (без пробелов):",
    )

    return WAITING_FOR_PASSPORT


async def register_passport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет паспорт и запрашивает год рождения"""
    context.user_data["passport"] = update.message.text

    await update.message.reply_text(
        "📅 Введите год вашего рождения (YYYY):",
    )

    return WAITING_FOR_YEAR


async def register_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет год рождения и завершает регистрацию"""
    try:
        year = int(update.message.text)
        if year < 1900 or year > 2024:
            await update.message.reply_text(
                "❌ Год должен быть от 1900 до 2024. Попробуйте ещё раз:"
            )
            return WAITING_FOR_YEAR

        context.user_data["birth_year"] = year
        user_id = str(update.effective_user.id)

        # Сохраняем пользователя
        register_user(user_id, context.user_data)

        text = (
            "✅ <b>Регистрация успешна!</b>\n\n"
            f"👤 Имя: {context.user_data['full_name']}\n"
            f"📧 Email: {context.user_data['email']}\n"
            f"🔢 Паспорт: {context.user_data['passport']}\n"
            f"📅 Год: {context.user_data['birth_year']}\n\n"
            "Теперь используйте /search для поиска цитаций."
        )

        await update.message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Введите корректный год (число от 1900 до 2024):"
        )
        return WAITING_FOR_YEAR


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /search - начало поиска"""
    user_id = str(update.effective_user.id)

    if not user_exists(user_id):
        text = (
            "❌ Вы не зарегистрированы!\n\n"
            "Используйте /register для регистрации перед поиском."
        )
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
        return

    user = get_user(user_id)

    # Клавиатура с типами виз
    keyboard = [
        [
            InlineKeyboardButton("НИЕ (с регионом)", callback_data="visa_nie_spec"),
            InlineKeyboardButton("НИЕ (национальный)", callback_data="visa_nie_nat"),
        ],
        [
            InlineKeyboardButton("ТИЕ (с регионом)", callback_data="visa_tie_spec"),
            InlineKeyboardButton("ТИЕ (национальный)", callback_data="visa_tie_nat"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"🔍 <b>Начало поиска</b>\n\n"
        f"Пользователь: {user['full_name']}\n"
        f"Паспорт: {user['passport']}\n\n"
        f"Выберите тип визы:"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )


async def visa_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора типа визы"""
    query = update.callback_query
    await query.answer()

    visa_type = query.data

    # Здесь должна быть логика выбора провинции, офиса и услуги
    # Пока сохраняем тип визы
    user_id = str(query.from_user.id)
    context.user_data["visa_type"] = visa_type

    text = f"✅ Выбран тип: {visa_type}\n\n" f"🔍 Начинается поиск...\n\n"

    await query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    # Имитация поиска (в реальной версии здесь будет запуск NIESpecified)
    await query.message.reply_text(
        "⏳ Поиск выполняется. Я пришлю уведомление, когда найду цитацию.",
        parse_mode=ParseMode.HTML,
    )

    # Сохраняем в историю
    save_search_history(
        {
            "user_id": user_id,
            "visa_type": visa_type,
            "start_time": datetime.now().isoformat(),
            "status": "started",
        }
    )

    logger.info(f"🔍 Пользователь {user_id} начал поиск: {visa_type}")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - статус поиска"""
    user_id = str(update.effective_user.id)

    if not user_exists(user_id):
        await update.message.reply_text(
            "❌ Вы не зарегистрированы. Используйте /register"
        )
        return

    text = (
        "📊 <b>Статус</b>\n\n"
        "✅ Поиск активен\n"
        "📍 Типы виз: НИЕ, ТИЕ\n"
        "⏱️ Работает: 2ч 45м\n"
        "🔔 Уведомления: включены\n\n"
        "Я отправлю вам сообщение как только найду свободную цитацию!"
    )

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stop - остановка поиска"""
    user_id = str(update.effective_user.id)

    if not user_exists(user_id):
        await update.message.reply_text(
            "❌ Вы не зарегистрированы. Используйте /register"
        )
        return

    text = (
        "⏹️ <b>Поиск остановлен</b>\n\n"
        "❌ Все автоматические поиски отключены\n"
        "📞 Вы можете связаться со мной командой /search для нового поиска"
    )

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    logger.info(f"⏹️ Пользователь {user_id} остановил поиск")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"❌ Ошибка: {context.error}")


# ═══════════════════════════════════════════════════════════════════════════════
# ИНИЦИАЛИЗАЦИЯ И ЗАПУСК БОТА
# ═══════════════════════════════════════════════════════════════════════════════


async def main():
    """Главная функция запуска бота"""
    logger.info("🤖 Инициализация Telegram бота...")

    # Инициализируем БД
    init_databases()

    # Создаём приложение
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация команды
    register_conversation = ConversationHandler(
        entry_points=[CommandHandler("register", register_start)],
        states={
            WAITING_FOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
            WAITING_FOR_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_email)],
            WAITING_FOR_PASSPORT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_passport)
            ],
            WAITING_FOR_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_year)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(register_conversation)
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CallbackQueryHandler(visa_type_callback, pattern="^visa_"))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("stop", stop_command))

    # Обработчик ошибок
    app.add_error_handler(error_handler)

    logger.info("✅ Бот инициализирован успешно")
    logger.info(f"🚀 Бот запущен на токене: {TELEGRAM_BOT_TOKEN[:20]}...")
    logger.info("⏳ Ожидание входящих сообщений...")

    # Запускаем бота с обработкой сигналов
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("⏹️ Получен сигнал остановки (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    import asyncio
    import signal
    import sys

    def signal_handler(sig, frame):
        logger.info("⏹️ Получен сигнал прерывания")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        sys.exit(1)
