# Модуль Modules

Специализированные модули для различных типов виз.

## Файлы

### base_visa.py
Абстрактный базовый класс для всех типов виз.
- Содержит общие методы работы с браузером:
  - `click_button()` - Клик по кнопке
  - `click_dropdown()` - Выбор опции из dropdown'а
  - `enter_text()` - Ввод текста в поле
- Обработка блокирующих состояний
- Логирование всех действий

### Подклассы (будут создаваться):
- `nie_specified.py` - НИЕ с привязкой к регионам
- `nie_national.py` - НИЕ национальный (без региона)
- `tie_specified.py` - ТИЕ с регионом
- `tie_national.py` - ТИЕ без региона

### Вспомогательные модули:
- `visa_factory.py` - Factory pattern для создания экземпляров
- `citation_extractor.py` - Парсер цитаций из HTML

## Пример использования (будущее)

```python
from modules.base_visa import BaseVisa
from selenium.webdriver.common.by import By

class NIESpecified(BaseVisa):
    def search_for_citations(self):
        # Реализация поиска цитаций
        pass

# Использование:
visa = NIESpecified('nie_specified', driver, start_url)
visa.click_button(actions, '//*[@id="button"]', "Нажать кнопку")
visa.enter_text(actions, '//*[@id="input"]', "Текст", "Поле ввода")
```
