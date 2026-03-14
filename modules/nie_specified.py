"""
Модуль для НИЕ (Número de Identidad de Extranjero) с указанием региона.

Класс для поиска цитаций для НИЕ в конкретном регионе и офисе.
Это специализированная виза, требует выбора провинции и офиса.
"""

import time
from random import randrange
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from modules.base_visa import BaseVisa
from modules.anti_blocking import (
    guard_blocking_states, 
    RestartLoopException,
    wait_clickable
)
from utils.wait import safe_wait_clickable
from utils.logger import setup_logger
from utils.block_handler import RestartLoop
from config.xpaths import get_xpaths

logger = setup_logger(__name__)


class NIESpecified(BaseVisa):
    """
    Класс для поиска цитаций НИЕ с указанием региона.
    
    Параметры в __init__:
        - driver: Selenium WebDriver
        - start_url: URL для перезагрузки при блокировке
        - passport: Номер паспорта (например, 'FV315480')
        - full_name: Полное имя (например, 'Yevhen Maksymov')
        - birth_year: Год рождения (например, '1991')
        - provincia: Индекс провинции (3 = Alicante)
        - oficina: Индекс офиса (13 = OEX Alicante)
        - tramite: Индекс типа услуги (5 = Police)
    """
    
    def __init__(self, driver, start_url: str, passport: str, full_name: str, 
                 birth_year: str, provincia: int, oficina: int, tramite: int):
        """
        Инициализация НИЕ с регионом.
        
        Args:
            driver: Selenium WebDriver объект
            start_url: Исходный URL для перезагрузки
            passport: Номер паспорта
            full_name: Полное имя (Фамилия Имя)
            birth_year: Год рождения (строка)
            provincia: Индекс провинции в dropdown'е
            oficina: Индекс офиса в dropdown'е
            tramite: Индекс типа услуги в dropdown'е
        """
        super().__init__('nie_specified', driver, start_url)
        
        # Параметры пользователя
        self.passport = passport
        self.full_name = full_name
        self.birth_year = birth_year
        self.provincia = provincia
        self.oficina = oficina
        self.tramite = tramite
        
        # Счётчик попыток
        self.attempt_counter = 0
        
        logger.info(f"Инициализирован NIESpecified для {full_name} (паспорт: {passport})")
        logger.info(f"  Провинция: {provincia}, Офис: {oficina}, Услуга: {tramite}")
    
    def close_cookie_popup(self, actions) -> bool:
        """
        Закрывает popup согласия с cookies.
        
        Returns:
            True если ошибка, False если успех
        """
        try:
            cookie_close = self.xpaths['cookie_close']
            element = self.driver.find_element(By.XPATH, cookie_close)
            actions.move_to_element(element).click().perform()
            logger.debug("✓ Cookie popup закрыт")
            time.sleep(0.1)
            return False
        except NoSuchElementException:
            logger.debug("  Cookie popup уже закрыт или отсутствует")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Ошибка при закрытии cookie: {e}")
            return False
    
    def select_provincia_and_accept(self, actions) -> None:
        """
        Выбирает провинцию и нажимает "Aceptar".
        
        Raises:
            RestartLoop: Если операция не удалась
        """
        try:
            # Проверяем блокировку перед попыткой выбора
            if guard_blocking_states(self.driver, self.start_url):
                logger.warning("[BLOCK] Блокировка обнаружена перед выбором провинции")
                raise RestartLoop("Блокировка: guard_blocking_states вернул True")
            
            # Выбирается провинция через form
            logger.debug(f"Выбираю провинцию {self.provincia}...")
            form_xpath = self.xpaths['form']
            
            # Пытаемся найти элемент
            try:
                dropdown_elem = self.driver.find_element(By.XPATH, form_xpath)
            except NoSuchElementException:
                # Элемент не найден - проверяем размер HTML
                page_source = self.driver.page_source
                if len(page_source) < 1000:
                    logger.error("⛔ Вероятно БЛОКИРОВКА: HTML слишком короткий")
                    logger.error(f"   Размер HTML: {len(page_source)} байт")
                    logger.error("   Сайт, вероятно, блокирует автоматизированный доступ")
                    logger.error("   Ожидаю 5 минут перед перезагрузкой...")
                    time.sleep(300)  # 5 минут
                    self.driver.get(self.start_url)  # Перезагружаем страницу
                    raise RestartLoop("Блокировка: HTML слишком короткий")
                else:
                    logger.error(f"❌ XPath не найден: {form_xpath}")
                    logger.error(f"   Размер HTML: {len(page_source)} байт")
                    raise RestartLoop("Элемент не найден - структура сайта изменилась")
            
            # Находим select внутри form и выбираем по индексу
            from selenium.webdriver.support.ui import Select
            select = Select(dropdown_elem)
            select.select_by_index(self.provincia)
            logger.info(f"✓ Провинция {self.provincia} выбрана")
            time.sleep(0.3)
            
            # Нажимаем кнопку Accept
            self.click_button(actions, self.xpaths['accept_button'], "Aceptar (провинция)", 0.5)
            logger.info("✓ Кнопка 'Aceptar' нажата")
            time.sleep(randrange(2, 5))
            
        except RestartLoopException as e:
            logger.warning(f"[ANTI-BLOCKING] Restart loop: {e}")
            raise RestartLoop(f"Anti-blocking: {e}")
        except Exception as e:
            logger.error(f"✗ Ошибка при выборе провинции: {e}")
            raise RestartLoop(f"Ошибка при выборе провинции")
    
    def select_oficina_and_tramite(self, actions) -> None:
        """
        Выбирает офис и тип услуги (трамите).
        
        Raises:
            RestartLoop: Если операция не удалась
        """
        try:
            # Дополнительное ожидание для загрузки страницы после выбора провинции
            logger.debug("⏳ Ожидание загрузки новых элементов (sede и tramiteGrupo)...")
            time.sleep(randrange(3, 5))
            
            # Выбираем офис
            logger.debug(f"Выбираю офис {self.oficina}...")
            logger.debug(f"   XPath для sede: {self.xpaths['office_dropdown']}")
            
            # Увеличиваем timeout для sede до 30 секунд - элемент может загружаться дольше
            try:
                office_element = safe_wait_clickable(self.driver, By.XPATH, self.xpaths['office_dropdown'], timeout=30)
                if office_element is None:
                    logger.error(f"✗ Офис dropdown (sede) не найден")
                    logger.error(f"   Проверяю наличие элемента на странице...")
                    try:
                        page_source = self.driver.page_source
                        if 'sede' in page_source:
                            logger.debug("   ℹ️ Элемент есть в HTML, но не кликабель")
                        else:
                            logger.error("   ⛔ Элемент отсутствует в HTML вообще!")
                    except:
                        pass
                    raise RestartLoop("Офис dropdown не найден")
                
                from selenium.webdriver.support.ui import Select
                select = Select(office_element)
                select.select_by_index(self.oficina)
                logger.info(f"✓ Офис {self.oficina} выбран")
            except Exception as e:
                logger.error(f"✗ Ошибка при выборе офиса: {e}")
                raise RestartLoop(f"Ошибка при выборе офиса: {e}")
            
            time.sleep(0.5)
            
            # Выбираем тип услуги (трамите)
            logger.debug(f"Выбираю услугу {self.tramite}...")
            logger.debug(f"   XPath для tramiteGrupo: {self.xpaths['service_dropdown']}")
            
            try:
                service_element = safe_wait_clickable(self.driver, By.XPATH, self.xpaths['service_dropdown'], timeout=30)
                if service_element is None:
                    logger.error(f"✗ Услуга dropdown (tramiteGrupo) не найдена")
                    raise RestartLoop("Услуга dropdown не найдена")
                
                from selenium.webdriver.support.ui import Select
                select = Select(service_element)
                select.select_by_index(self.tramite)
                logger.info(f"✓ Услуга {self.tramite} выбрана")
            except Exception as e:
                logger.error(f"✗ Ошибка при выборе услуги: {e}")
                raise RestartLoop(f"Ошибка при выборе услуги: {e}")
            
            time.sleep(0.3)
            
            # Нажимаем Accept
            self.click_button(actions, self.xpaths['accept_button'], "Aceptar (офис)", 0.5)
            logger.info("✓ Кнопка 'Aceptar' нажата (офис)")
            time.sleep(randrange(2, 4))
            
        except RestartLoop:
            raise
        except Exception as e:
            logger.error(f"✗ Ошибка при выборе офиса/услуги: {e}")
            raise RestartLoop(f"Ошибка при выборе офиса/услуги")
    
    def enter_person_data(self, actions) -> None:
        """
        Выбирает тип лица (радиокнопка) и вводит данные паспорта.
        
        Raises:
            RestartLoop: Если операция не удалась
        """
        try:
            # Нажимаем кнопку Enter
            logger.debug("Нажимаю кнопку 'Entrar'...")
            self.click_button(actions, self.xpaths['enter_button'], "Entrar", 1.0)
            logger.info("✓ Кнопка 'Entrar' нажата")
            time.sleep(2)
            
            # Выбираем тип лица (вторая опция - иностранец)
            logger.debug("Выбираю тип лица 'Extranjero'...")
            self.click_button(actions, self.xpaths['person_type_radio'], "Радиокнопка Extranjero", 0.3)
            logger.info("✓ Тип лица выбран (Extranjero)")
            
            # Вводим паспорт
            logger.debug(f"Ввожу паспорт: {self.passport}")
            self.enter_text(actions, self.xpaths['passport_input'], self.passport, "Паспорт")
            logger.info(f"✓ Паспорт введён: {self.passport}")
            
            # Вводим имя и фамилию
            logger.debug(f"Ввожу имя: {self.full_name}")
            self.enter_text(actions, self.xpaths['name_surname_input'], self.full_name, "Имя и Фамилия")
            logger.info(f"✓ Имя введено: {self.full_name}")
            
            # Вводим год рождения
            logger.debug(f"Ввожу год рождения: {self.birth_year}")
            self.enter_text(actions, self.xpaths['birth_year_input'], self.birth_year, "Год рождения")
            logger.info(f"✓ Год рождения введён: {self.birth_year}")
            
        except RestartLoop:
            raise
        except Exception as e:
            logger.error(f"✗ Ошибка при вводе данных: {e}")
            raise RestartLoop(f"Ошибка при вводе данных лица")
    
    def submit_form(self, actions) -> None:
        """
        Отправляет форму дважды (как в оригинальном коде).
        
        Raises:
            RestartLoop: Если операция не удалась
        """
        try:
            # Первый submit
            logger.debug("Первый submit формы...")
            self.click_button(actions, self.xpaths['submit_button'], "Enviar (1)", 0.5)
            logger.info("✓ Первый submit выполнен")
            time.sleep(randrange(2, 3))
            
            # Второй submit
            logger.debug("Второй submit формы...")
            self.click_button(actions, self.xpaths['submit_button'], "Enviar (2)", 0.5)
            logger.info("✓ Второй submit выполнен")
            
        except RestartLoop:
            raise
        except Exception as e:
            logger.error(f"✗ Ошибка при отправке формы: {e}")
            raise RestartLoop(f"Ошибка при отправке формы")
    
    def check_citations_available(self, actions) -> bool:
        """
        Проверяет, доступны ли цитации на странице.
        
        Returns:
            True если цитации найдены, False если нет цитаций
        """
        try:
            error_element = self.driver.find_element(By.XPATH, self.xpaths['error_message'])
            error_text = error_element.text
            
            if 'En este momento no hay citas' in error_text:
                logger.warning("⚠️ В данный момент нет доступных цитаций")
                return False
            else:
                logger.info(f"ℹ️ Сообщение с сервера: {error_text}")
                return False
                
        except NoSuchElementException:
            # Элемент с сообщением "нет цитаций" не найден
            # Значит, цитации доступны!
            logger.info("🎉 ЦИТАЦИИ НАЙДЕНЫ! Требуется проверка вручную!")
            return True
        except Exception as e:
            logger.error(f"⚠️ Ошибка при проверке цитаций: {e}")
            return False
    
    def handle_citations_found(self):
        """
        Обработчик когда цитации найдены.
        В будущем можно добавить отправку в Telegram.
        """
        logger.critical("🎯🎯🎯 ЦИТАЦИИ НАЙДЕНЫ! 🎯🎯🎯")
        logger.critical(f"   Паспорт: {self.passport}")
        logger.critical(f"   Имя: {self.full_name}")
        logger.critical(f"   Провинция: {self.provincia}, Офис: {self.oficina}")
        
        # TODO: Отправить уведомление в Telegram
        # TODO: Сохранить информацию в БД
        
        # Для теста: выводим в консоль и ждём
        print("\n" + "="*60)
        print("🎉 ЦИТАЦИИ НАЙДЕНЫ! 🎉")
        print("="*60 + "\n")
    
    def exit_and_restart(self, actions) -> None:
        """
        Нажимает кнопку выхода для перезагрузки цикла.
        
        Raises:
            RestartLoop: Для перезагрузки цикла
        """
        try:
            exit_button = self.xpaths['exit_button']
            exit_elem = self.driver.find_element(By.XPATH, exit_button)
            actions.move_to_element(exit_elem).click().perform()
            logger.info("✓ Нажата кнопка выхода (Salir)")
        except NoSuchElementException:
            logger.warning("⚠️ Кнопка выхода не найдена")
        except Exception as e:
            logger.warning(f"⚠️ Ошибка при нажатии выхода: {e}")
        
        raise RestartLoop("Перезагружаю цикл поиска")
    
    def search_for_citations(self):
        """
        Основной цикл поиска цитаций.
        
        Работает в бесконечном цикле пока не будут найдены цитации.
        Использует uc_open_with_reconnect() для переподключения при блокировке.
        
        Может быть остановлен через Ctrl+C.
        """
        logger.info("="*60)
        logger.info("🚀 Запуск поиска цитаций для НИЕ с регионом")
        logger.info("🔍 Нажми Ctrl+C для остановки поиска")
        logger.info("="*60)
        
        actions = ActionChains(self.driver)
        
        try:
            while True:
                try:
                    self.attempt_counter += 1
                    
                    logger.info(f"\n#{self.attempt_counter} ПОПЫТКА ПОИСКА")
                    logger.debug("-" * 60)
                    
                    # Задержка между попытками для anti-detection (4-7 сек как в v1.0)
                    time.sleep(randrange(4, 7))
                    
                    # ВАЖНО: Проверяем блокировку перед каждой попыткой
                    # guard_blocking_states() автоматически ждет нужное время и перезагружает страницу
                    if guard_blocking_states(self.driver, self.start_url):
                        logger.info("↻ Блокировка обнаружена и обработана, продолжаю...")
                        continue
                    
                    # Проверяем дополнительно 429 в странице
                    try:
                        page_source = self.driver.page_source
                        if "429" in page_source or "Too Many Requests" in page_source:
                            logger.error("⛔ БЛОКИРОВКА: Сайт вернул 429 (Too Many Requests)")
                            logger.error("⏳ Ожидание 10 минут перед попыткой...")
                            time.sleep(600)  # 10 минут
                            self.driver.get(self.start_url)
                            continue
                    except Exception as e:
                        logger.debug(f"Ошибка при проверке блокировки: {e}")
                    
                    # 1. Закрываем cookie popup
                    self.close_cookie_popup(actions)
                    
                    # Случайная задержка
                    time.sleep(randrange(3, 6))
                    
                    # 2. Выбираем провинцию и нажимаем Accept
                    self.select_provincia_and_accept(actions)
                    
                    # 3. Выбираем офис и услугу
                    self.select_oficina_and_tramite(actions)
                    
                    # 4. Вводим данные лица
                    self.enter_person_data(actions)
                    
                    # 5. Отправляем форму
                    self.submit_form(actions)
                    
                    # 6. Проверяем доступность цитаций
                    citations_found = self.check_citations_available(actions)
                    
                    if citations_found:
                        # ЦИТАЦИИ НАЙДЕНЫ!
                        self.handle_citations_found()
                        # Ждём перед перезагрузкой
                        time.sleep(60)
                    else:
                        # Нет цитаций, перезагружаем
                        self.exit_and_restart(actions)
                    
                except RestartLoopException as e:
                    logger.debug(f"[ANTI-BLOCKING] RestartLoop: {e}")
                    time.sleep(randrange(60, 120))  # 1-2 минуты между попытками
                    continue
                
                except RestartLoop as e:
                    logger.debug(f"🔄 RestartLoop: {e}")
                    time.sleep(randrange(60, 120))  # 1-2 минуты между попытками
                    continue
                    
                except Exception as e:
                    logger.error(f"❌ Неожиданная ошибка в цикле: {type(e).__name__}: {e}")
                    logger.debug("Перезагружаю через 30 секунд...")
                    time.sleep(30)
                    continue
        
        except KeyboardInterrupt:
            logger.warning("\n\n⚠️ ПОИСК ОСТАНОВЛЕН ПОЛЬЗОВАТЕЛЕМ (Ctrl+C)")
            logger.warning("🔚 Закрываю браузер...")
            try:
                self.driver.quit()
                logger.info("✅ Браузер закрыт")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при закрытии браузера: {e}")
            return None
