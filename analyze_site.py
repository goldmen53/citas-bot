"""
Скрипт для анализа реальной структуры сайта испанского сервиса
и выяснения какие XPath'ы работают
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Настройка Chrome
chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

print("🔧 Создаю WebDriver...")
try:
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ WebDriver создан")
except Exception as e:
    print(f"❌ Ошибка создания WebDriver: {e}")
    print("💡 Попробуй установить ChromeDriver:")
    print("   pip install webdriver-manager")
    exit(1)

try:
    print("\n🌐 Загружаю страницу...")
    print("⏳ Ожидание 5 секунд перед доступом (чтобы избежать блокировки)...")
    time.sleep(5)
    
    driver.get("https://icp.administracionelectronica.gob.es/icpco/index")
    
    print("⏳ Ожидание загрузки страницы (10 секунд для JavaScript)...")
    time.sleep(10)
    
    print("✅ Страница загружена")
    
    # Сохраняем HTML
    html = driver.page_source
    
    # Проверяем есть ли признаки блокировки
    if "429" in html or "Too Many Requests" in html or "blocked" in html.lower():
        print("⚠️ БЛОКИРОВКА: Сайт заблокировал доступ!")
        print("💡 Подожди 10-15 минут и попробуй снова")
    elif len(html) < 1000:
        print("⚠️ ПОДОЗРЕНИЕ НА БЛОКИРОВКУ: HTML очень короткий")
        print(f"   Размер HTML: {len(html)} байт")
        print("💡 Возможно сайт блокирует автоматизированный доступ")
    
    with open('/tmp/site_analysis.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"📄 HTML сохранен в /tmp/site_analysis.html ({len(html)} байт)")
    
    # Проверяем наличие основных элементов
    print("\n🔍 Проверяю наличие элементов...\n")
    
    test_xpaths = {
        'Form ID': '//*[@id="form"]',
        'Accept Button': '//*[@id="btnAceptar"]',
        'Passport Input': '//*[@id="txtIdCitado"]',
        'Name Input': '//*[@id="txtDesCitado"]',
        'Birth Year Input': '//*[@id="txtAnnoCitado"]',
        'Submit Button': '//*[@id="btnEnviar"]',
        'Office Dropdown': '//*[@id="sede"]',
        'Service Dropdown': '//*[@id="tramiteGrupo[1]"]',
        'Enter Button': '//*[@id="btnEntrar"]',
    }
    
    for name, xpath in test_xpaths.items():
        try:
            from selenium.webdriver.common.by import By
            element = driver.find_element(By.XPATH, xpath)
            print(f"✅ {name:25} НАЙДЕН   | XPath: {xpath}")
        except Exception as e:
            print(f"❌ {name:25} НЕ НАЙДЕН | XPath: {xpath}")
            print(f"   Ошибка: {str(e)[:80]}")
    
    # Пытаемся найти форму другими способами
    print("\n\n🔎 Альтернативные способы найти форму:\n")
    
    alternative_xpaths = {
        'Form by tag (любая форма)': '//form',
        'Form by action': '//form[@action]',
        'All divs with id': '//*[@id]',
        'Buttons': '//button',
        'Input fields': '//input',
    }
    
    for name, xpath in alternative_xpaths.items():
        try:
            from selenium.webdriver.common.by import By
            elements = driver.find_elements(By.XPATH, xpath)
            print(f"🔍 {name:30} НАЙДЕНО: {len(elements)} элементов")
            if len(elements) > 0 and len(elements) <= 10:
                for i, el in enumerate(elements[:5]):
                    try:
                        el_id = el.get_attribute('id')
                        el_class = el.get_attribute('class')
                        el_type = el.get_attribute('type')
                        el_name = el.get_attribute('name')
                        print(f"   [{i}] ID={el_id}, Class={el_class}, Type={el_type}, Name={el_name}")
                    except:
                        pass
        except Exception as e:
            print(f"❌ {name:30} Ошибка: {str(e)[:60]}")
    
    print("\n✅ Анализ завершен")
    print("📄 Полный HTML сохранен: /tmp/site_analysis.html")
    print("📌 Используй Firefox DevTools или сохраненный HTML для анализа структуры")
    
finally:
    print("\n🔚 Закрываю браузер...")
    driver.quit()
    print("✅ Браузер закрыт")
