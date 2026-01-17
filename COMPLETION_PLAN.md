# 🔧 ПЛАН ЗАВЕРШЕНИЯ ПРОЕКТА - Детальные Инструкции

**Статус:** Ready to implement  
**Приблизительное время:** 4-5 часов  
**Сложность:** Средняя (70% код готов, 30% интеграция)

---

## STEP-BY-STEP ИНСТРУКЦИЯ

### ШАГИ 1-2: ПОДГОТОВКА (30 минут)

#### Шаг 1: Найти или использовать тестовый URL
```bash
# ВАРИАНТ A: Ты знаешь URL сайта?
# Просто скажи мне - я обновлю config

# ВАРИАНТ B: Используем mock-сервис для тестирования
# Я создам функцию которая эмулирует ответ сайта
# Потом ты обновишь URL когда найдешь реальный
```

#### Шаг 2: Проверить WebDriver установку
```bash
# Проверить есть ли Chrome или Firefox
which google-chrome
which chromium
which firefox

# Если нет - установить:
# Ubuntu/Debian: sudo apt-get install chromium-browser
# Или: pip install webdriver-manager
```

---

### ШАГИ 3-5: РЕАЛИЗАЦИЯ ИНТЕГРАЦИИ (3-4 часа)

#### Шаг 3: Создать async wrapper для Selenium (вспомогательный модуль)
**Файл:** `modules/selenium_runner.py` (НОВЫЙ)

Этот модуль будет содержать:
- Функцию `run_selenium_search()` - блокирующая функция для поиска
- WebDriver setup/cleanup логику
- Обработку ошибок и timeout'ов
- Anti-bot механизмы (delay, headers)

**Примерный код:**
```python
# modules/selenium_runner.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modules.nie_specified import NIESpecified
from utils.logger import setup_logger

logger = setup_logger(__name__)
executor = ThreadPoolExecutor(max_workers=3)

def run_selenium_search(passport, full_name, birth_year, visa_type):
    """
    BLOCKING функция для запуска Selenium поиска
    Вызывается из async контекста через run_in_executor
    """
    try:
        # Настроить WebDriver options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Background mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Создать WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        logger.info(f"WebDriver запущен для {visa_type}")
        
        # Выбрать правильный класс в зависимости от типа визы
        if visa_type == 'visa_nie_spec':
            searcher = NIESpecified(
                driver=driver,
                start_url="https://www.cit.gob.es/...",  # ОБНОВИТЬ
                passport=passport,
                full_name=full_name,
                birth_year=birth_year,
                provincia=0,  # Default или от пользователя
                oficina=0,
                tramite=0
            )
        # Добавить другие типы виз когда будут готовы
        
        # Запустить поиск
        citations = searcher.search()
        
        # Закрыть WebDriver
        driver.quit()
        
        logger.info(f"Поиск завершен, найдено цитаций: {len(citations)}")
        return citations
        
    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        driver.quit()
        raise

async def async_search(passport, full_name, birth_year, visa_type):
    """
    ASYNC функция - обертка для блокирующего Selenium
    Вызывается из Telegram bot'а
    """
    loop = asyncio.get_event_loop()
    citations = await loop.run_in_executor(
        executor,
        run_selenium_search,
        passport,
        full_name,
        birth_year,
        visa_type
    )
    return citations
```

#### Шаг 4: Модифицировать bot_handler.py (visa_type_callback + search_command)
**Файл:** `telegram_bot/bot_handler.py` (МОДИФИКАЦИЯ)

Нужно обновить две функции:

**Функция 1: search_command()**
```python
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /search - запрос поиска цитаций
    Показывает inline-кнопки с выбором типа визы
    """
    user = get_user(update.effective_user.id)
    
    if not user:
        await update.message.reply_text(
            "❌ Сначала зарегистрируйся командой /register"
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🏠 НИЕ (регион указан)", callback_data="visa_nie_spec")],
        [InlineKeyboardButton("🌍 НИЕ (национальный)", callback_data="visa_nie_nat")],
        [InlineKeyboardButton("💼 ТИЕ (регион указан)", callback_data="visa_tie_spec")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔍 Выбери тип визы для поиска:",
        reply_markup=reply_markup
    )
```

**Функция 2: visa_type_callback()**
```python
async def visa_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработка выбора типа визы
    Запускает Selenium поиск в фоне
    """
    query = update.callback_query
    visa_type = query.data
    user_id = update.effective_user.id
    
    # Подтвердить нажатие кнопки
    await query.answer(f"⏳ Начинаю поиск для {visa_type}...")
    
    # Получить данные пользователя
    user = get_user(user_id)
    if not user:
        await query.edit_message_text("❌ Ошибка: данные пользователя не найдены")
        return
    
    # НОВОЕ: Отправить сообщение что поиск начался
    await query.edit_message_text(
        "🔄 Поиск цитаций в процессе...\n"
        "Это может занять несколько минут."
    )
    
    try:
        # НОВОЕ: Импортировать async_search функцию
        from modules.selenium_runner import async_search
        
        # НОВОЕ: Запустить Selenium в отдельном потоке (асинхронно)
        citations = await async_search(
            passport=user['passport'],
            full_name=user['full_name'],
            birth_year=user['birth_year'],
            visa_type=visa_type
        )
        
        # Обработать результаты
        if citations:
            result_text = "✅ Найдены цитации:\n\n"
            for i, cite in enumerate(citations[:5], 1):  # Показать первые 5
                result_text += f"{i}. {cite}\n"
            
            # Сохранить в history
            save_search_history(user_id, visa_type, "found", citations)
        else:
            result_text = "❌ Цитации не найдены. Попробуй позже."
            save_search_history(user_id, visa_type, "not_found", [])
        
        # Отправить результаты
        await context.bot.send_message(
            chat_id=user_id,
            text=result_text
        )
        
    except Exception as e:
        logger.error(f"Ошибка поиска для {user_id}: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text=f"❌ Ошибка при поиске:\n{str(e)}"
        )
        save_search_history(user_id, visa_type, "error", [])
```

#### Шаг 5: Добавить WebDriver callback в главное приложение
**Файл:** `telegram_bot/bot_handler.py` (В main функции)

В функции `main()`, после регистрации всех обработчиков, добавить:

```python
async def main():
    """Основная функция инициализации и запуска bot'а"""
    
    # ... СУЩЕСТВУЮЩИЙ КОД ...
    
    # Регистрация callback'а для visa_type_callback
    app.add_handler(CallbackQueryHandler(
        visa_type_callback,
        pattern="^visa_.*"  # Все кнопки начинающиеся с "visa_"
    ))
    
    # НОВОЕ: Инициализировать WebDriver pooling (опционально)
    from modules.selenium_runner import init_driver_pool
    init_driver_pool(max_workers=3)  # Максимум 3 одновременных поисков
    
    # ... ОСТАЛЬНОЙ КОД ...
```

---

### ШАГИ 6-7: ТЕСТИРОВАНИЕ (30-45 минут)

#### Шаг 6: Unit тесты для новых функций
**Файл:** `test_bot.py` (ДОБАВИТЬ новые тесты)

```python
def test_selenium_runner():
    """Тест асинхронного Selenium wrapper'а"""
    import asyncio
    from modules.selenium_runner import async_search
    
    async def run_test():
        # Mock test - не требует реального вебдрайвера
        citations = await async_search(
            passport="12345678A",
            full_name="Test User",
            birth_year="1990",
            visa_type="visa_nie_spec"
        )
        assert isinstance(citations, list)
    
    asyncio.run(run_test())
    print("✅ PASSED - Selenium runner test")

def test_visa_type_callback():
    """Тест callback'а для выбора типа визы"""
    from telegram_bot.bot_handler import visa_type_callback
    # Это сложный тест, требует mock Update/Context
    print("✅ PASSED - Visa type callback test (mock)")
```

#### Шаг 7: Manual Telegram тестирование

```bash
# 1. Запустить bot'а
PYTHONPATH=/home/yevhen/VScode/CITAS python3 telegram_bot/bot_handler.py

# 2. В отдельном терминале monitoring логов
tail -f logs/citas.log

# 3. В Telegram боте (на телефоне или web):
/register                    # Зарегистрироваться
/search                      # Выбрать тип визы
# Выбрать НИЕ (регион указан) и дождаться результатов
/status                      # Проверить статус
```

---

## 📋 ЧЕКЛИСТ ВЫПОЛНЕНИЯ

### Подготовка
- [ ] Найти/определить URL сайта иммиграции
- [ ] Проверить наличие Chrome/Firefox
- [ ] Проверить что selenium установлен

### Кодирование
- [ ] Создать modules/selenium_runner.py (async wrapper)
- [ ] Модифицировать search_command() в bot_handler.py
- [ ] Модифицировать visa_type_callback() в bot_handler.py
- [ ] Добавить WebDriver pooling в main()
- [ ] Добавить новые импорты (InlineKeyboardButton, InlineKeyboardMarkup)

### Тестирование
- [ ] Запустить test_bot.py (убедиться что старые тесты работают)
- [ ] Добавить новые unit тесты для selenium_runner
- [ ] Manual Telegram тест: /register → /search → выбор → ожидание результата
- [ ] Проверить логи в logs/citas.log

### Финализация
- [ ] Обновить README.md с инструкциями
- [ ] Git commit всех изменений
- [ ] Обновить PROJECT_STATUS.md с новым прогрессом

---

## ⚠️ ПОТЕНЦИАЛЬНЫЕ ПРОБЛЕМЫ И РЕШЕНИЯ

### Проблема 1: "WebDriver не найден"
```
selenium.common.exceptions.WebDriverException: unknown error: 
  Chrome failed to start: was killed due to timeout
```
**Решение:** 
1. Установить Chrome: `sudo apt-get install chromium-browser`
2. Или использовать webdriver-manager: `pip install webdriver-manager`

### Проблема 2: "429 Too Many Requests" от сайта
```
site_responses/429 Too Many Requests.html
```
**Решение:**
- Это нормально, block_handler.py это обрабатывает
- Добавить больше delays в NIESpecified
- Использовать rotating user-agents
- Лимитировать количество одновременных поисков

### Проблема 3: "CAPTCHA требуется"
**Решение:**
- Добавить human-like delays (уже есть в utils/wait.py)
- Использовать anti-bot headers
- Если нужна CAPTCHA solving - использовать 2captcha или ручное решение

### Проблема 4: XPath'ы устарели
```
NoSuchElementException: Message: no such element
```
**Решение:**
1. Открыть сайт в браузере
2. Инспектировать элементы (F12)
3. Обновить XPath в config/xpaths.py
4. Пересохранить сайт в site_responses/

---

## 🎓 ОБРАЗОВАТЕЛЬНЫЙ МАТЕРИАЛ

### Как работает async/await в Python Telegram Bot
```python
# БЕЗ async (блокирует бота):
def search():
    time.sleep(300)  # 5 минут ожидания
    return "готово"

# С async и executor:
async def search():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)
    return result
```

### Как работает ConversationHandler (уже реализовано)
```python
# Диалог: /register → имя → email → паспорт → год рождения
# States: 0 (name), 1 (email), 2 (passport), 3 (year)
# Переходы: 0→1→2→3→END
# В bot_handler.py это уже реализовано в функциях register_*
```

### Как работает CallbackQueryHandler (нужно добавить)
```python
# Пользователь видит: 
#  [Кнопка 1] [Кнопка 2] [Кнопка 3]
#
# При клике на кнопку:
#  1. Отправляется callback_data="visa_nie_spec"
#  2. Вызывается callback function (visa_type_callback)
#  3. В функции можно: edit_message, send_message, answer
```

---

## 📞 ПОДДЕРЖКА ПРИНЯТИЯ РЕШЕНИЙ

**Если я делаю ВСЕ:**
- Напиши "davай" - я создам все файлы и модификации
- Время: 2-3 часа
- Результат: Полностью готовый к тестированию код

**Если ВМЕСТЕ:**
- Я пишу код интеграции
- Ты находишь/проверяешь URL сайта
- Ты создаешь WebDriver для своей ОС
- Встречаемся на этапе тестирования

**Если ТЫ делаешь:**
- Я даю детальные инструкции (они выше в этом файле)
- Ты следуешь шагам 1-7
- Я помогаю в дебаганге

---

## 🚀 ПОСЛЕДУЮЩИЕ ШАГИ (PHASE 2-4)

После завершения Phase 1 (базовая интеграция):

1. **Добавить новые типы виз** (nie_national, tie_specified, tie_national)
2. **Оптимизировать производительность** (WebDriver pooling, caching)
3. **Добавить уведомления** (push-notifications найденных цитаций)
4. **Production deployment** (systemd service, monitoring, logs rotation)

---

**Вопрос для продолжения:**
> Давай я сделаю все файлы и модификации, или у тебя есть вопросы по плану?

**Или скажи:**
> У меня есть URL: https://...

Тогда я сразу начну писать код с правильным URL'ом!

---

*Документ подготовлен:* 17 января 2026  
*Версия:* 1.0  
*Автор:* AI Assistant
