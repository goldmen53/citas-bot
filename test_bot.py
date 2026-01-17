#!/usr/bin/env python3
"""
Тестирование Telegram бота
Проверяет инициализацию, БД, команды и интеграцию
"""

import sys
import os
import json
from pathlib import Path

# Добавляем проект в PYTHONPATH
sys.path.insert(0, '/home/yevhen/VScode/CITAS')

# Импортируем нужные модули
from utils.logger import setup_logger
from telegram_bot.bot_handler import (
    init_databases, 
    load_users, 
    register_user,
    save_search_history,
    USERS_DB,
    SEARCH_HISTORY_DB
)

logger = setup_logger("test_telegram_bot")

# ═══════════════════════════════════════════════════════════════════════════════
# ТЕСТЫ
# ═══════════════════════════════════════════════════════════════════════════════

def test_databases():
    """Тест инициализации БД"""
    print("\n🧪 TEST 1: Инициализация БД")
    print("─" * 70)
    
    try:
        init_databases()
        
        # Проверяем что файлы созданы
        assert USERS_DB.exists(), f"❌ {USERS_DB} не создан"
        assert SEARCH_HISTORY_DB.exists(), f"❌ {SEARCH_HISTORY_DB} не создан"
        
        print(f"✅ users.json создан: {USERS_DB}")
        print(f"✅ search_history.json создан: {SEARCH_HISTORY_DB}")
        
        # Проверяем что они валидные JSON
        with open(USERS_DB) as f:
            users = json.load(f)
        with open(SEARCH_HISTORY_DB) as f:
            history = json.load(f)
        
        print(f"✅ Оба файла содержат валидный JSON")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def test_user_registration():
    """Тест регистрации пользователя"""
    print("\n🧪 TEST 2: Регистрация пользователя")
    print("─" * 70)
    
    try:
        test_user_id = "123456789"
        test_user_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "passport": "12345678A",
            "birth_year": 1990
        }
        
        # Регистрируем пользователя
        register_user(test_user_id, test_user_data)
        print(f"✅ Пользователь {test_user_id} зарегистрирован")
        
        # Проверяем что данные сохранились
        users = load_users()
        assert test_user_id in users, "❌ Пользователь не найден в БД"
        assert users[test_user_id]["full_name"] == "Test User"
        
        print(f"✅ Данные пользователя сохранены корректно:")
        print(f"   • Имя: {users[test_user_id]['full_name']}")
        print(f"   • Email: {users[test_user_id]['email']}")
        print(f"   • Паспорт: {users[test_user_id]['passport']}")
        print(f"   • Год: {users[test_user_id]['birth_year']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def test_search_history():
    """Тест истории поисков"""
    print("\n🧪 TEST 3: История поисков")
    print("─" * 70)
    
    try:
        test_record = {
            "user_id": "123456789",
            "visa_type": "visa_nie_spec",
            "start_time": "2026-01-17T19:02:00",
            "status": "started"
        }
        
        # Добавляем запись в историю
        save_search_history(test_record)
        print(f"✅ Запись в историю добавлена")
        
        # Проверяем что запись сохранилась
        with open(SEARCH_HISTORY_DB) as f:
            history = json.load(f)
        
        assert len(history) > 0, "❌ История пуста"
        assert history[-1]["user_id"] == "123456789"
        
        print(f"✅ Данные в истории:")
        print(f"   • User ID: {history[-1]['user_id']}")
        print(f"   • Тип визы: {history[-1]['visa_type']}")
        print(f"   • Статус: {history[-1]['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def test_env_config():
    """Тест конфигурации .env"""
    print("\n🧪 TEST 4: Конфигурация .env")
    print("─" * 70)
    
    try:
        from dotenv import load_dotenv
        
        load_dotenv()
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        assert token, "❌ TELEGRAM_BOT_TOKEN не найден"
        assert chat_id, "❌ TELEGRAM_CHAT_ID не найден"
        
        # Показываем частично для безопасности
        token_preview = token[:15] + "..." if token else "N/A"
        print(f"✅ TELEGRAM_BOT_TOKEN загружен: {token_preview}")
        print(f"✅ TELEGRAM_CHAT_ID загружен: {chat_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def test_imports():
    """Тест импорта всех модулей"""
    print("\n🧪 TEST 5: Импорт модулей")
    print("─" * 70)
    
    try:
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler
        print(f"✅ python-telegram-bot импортирован")
        
        from utils.logger import setup_logger
        print(f"✅ utils.logger импортирован")
        
        from config.xpaths import get_xpaths
        print(f"✅ config.xpaths импортирован")
        
        from modules.base_visa import BaseVisa
        print(f"✅ modules.base_visa импортирован")
        
        from modules.nie_specified import NIESpecified
        print(f"✅ modules.nie_specified импортирован")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def test_bot_initialization():
    """Тест инициализации бота"""
    print("\n🧪 TEST 6: Инициализация бота")
    print("─" * 70)
    
    try:
        from telegram.ext import Application
        from dotenv import load_dotenv
        
        load_dotenv()
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        # Создаём приложение (но не запускаем polling)
        app = Application.builder().token(token).build()
        
        print(f"✅ Приложение Telegram инициализировано")
        print(f"✅ Обработчики готовы к регистрации")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ЗАПУСК ТЕСТОВ
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "═" * 70)
    print("    🧪 TELEGRAM БОТ - ТЕСТИРОВАНИЕ")
    print("═" * 70)
    
    tests = [
        ("Инициализация БД", test_databases),
        ("Регистрация пользователя", test_user_registration),
        ("История поисков", test_search_history),
        ("Конфигурация .env", test_env_config),
        ("Импорт модулей", test_imports),
        ("Инициализация бота", test_bot_initialization),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"❌ Критическая ошибка в {name}: {e}")
            results.append((name, False))
    
    # Итоги
    print("\n" + "═" * 70)
    print("    📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("═" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12} {name}")
    
    print("─" * 70)
    print(f"Итого: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 БОТ ГОТОВ К ИСПОЛЬЗОВАНИЮ")
        return 0
    else:
        print(f"\n❌ {total - passed} тест(ов) не пройдено")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
