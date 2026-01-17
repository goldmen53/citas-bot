from random import randrange
from selenium import webdriver
import time
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import subprocess
from selenium.webdriver.support.ui import Select
import pygame
from seleniumbase import Driver
from selenium.common.exceptions import NoSuchElementException


class RestartLoop(Exception):
    pass


def safe_wait_clickable(driver, by, value, timeout=30):
    if guard_blocking_states(driver,START_URL):
        raise RestartLoop # Прерываем ожидание, если сайт нас заблокировал

    try:
        return wait_clickable(driver, by, value, timeout)
    except Exception: # Перехватываем TimeoutException и прочие
        print(f'[TIMEOUT] Element not clickable: {value}')
        raise RestartLoop
def wait_clickable(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


    try:
        f_element=driver.find_element(By.XPATH, '/html/body/h1')
        if f_element.text == 'Too Many Requests':
            print("Too Many Requests")
            time.sleep(310)
            driver.navigate().refresh()
    except:
        pass
def guard_blocking_states(driver,start_url):
    # --- Go Back / Request Rejected ---
    
    try:
        el = driver.find_element(By.XPATH, '/html/body/a')
        if el.text.strip() == '[Go Back]':
            print('[BLOCK] Request rejected → waiting 610s')
            time.sleep(610)

            print('[BLOCK] Reopening start page')
            driver.get(start_url)
            return True
    except NoSuchElementException:
        pass

    # --- Too Many Requests ---
    try:
        el = driver.find_element(By.XPATH, '/html/body/h1')
        if el.text.strip() == 'Too Many Requests':
            print('[BLOCK] Too Many Requests → waiting 310s')
            time.sleep(310)

            print('[BLOCK] Reopening start page')
            driver.get(start_url)
            return True
    except NoSuchElementException:
        pass

    return False

def click_button(actions,driver,path,by_type=By.XPATH):
    if guard_blocking_states(driver,START_URL):
        return True
    # try:
    f_element = wait_clickable(driver,by_type,path)
    actions.move_to_element(f_element).click().perform()
    time.sleep(0.1)
    # except:
    #       pass
    return False
def click_dropdown(actions,driver, path, n_drop, by_type=By.XPATH):
    if guard_blocking_states(driver,START_URL):
        return True
    f_element = safe_wait_clickable(driver, by_type, path)
    actions.move_to_element(f_element).perform()
    dropdown = Select(f_element)
    dropdown.select_by_visible_text(n_drop) if isinstance(n_drop, str) else dropdown.select_by_index(n_drop)
    
    time.sleep(0.1)
    return False

def enter_text(actions,driver, path, text, by_type=By.XPATH):
    if guard_blocking_states(driver,START_URL):
        return True
        
    f_element = wait_clickable(driver, by_type, path)
    actions.move_to_element(f_element).click().perform()
    f_element.clear() # Желательно очистить поле перед вводом
    f_element.send_keys(str(text))
    return False

START_URL = 'https://icp.administracionelectronica.gob.es/icpco/index'


if __name__ == '__main__':
    START_URL = 'https://icp.administracionelectronica.gob.es/icpco/index'
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(START_URL, 5)
    actions = ActionChains(driver)
    
    counter=0

    while True:    
        time.sleep(randrange(4,7))   
        counter+=1
        print(f'Количество попыток: {counter}')
        
        actions = ActionChains(driver)

        if guard_blocking_states(driver):
            continue

        try:
            #cookies_accept
            f_element = wait_clickable(driver,By.XPATH,'//*[@id="cookie_action_close_header"]')

            actions.move_to_element(f_element).click().perform()
            time.sleep(0.1)
        except:
            pass

        #provincia
        try:
            f_element = safe_wait_clickable(By.XPATH, '//*[@id="form"]')
        except RestartLoop:
            continue
        dropdown = Select(f_element)
        dropdown.select_by_index(3)

        time.sleep(0.1)

        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnAceptar"]')
        actions.move_to_element(f_element).click().perform()

        time.sleep(randrange(2,5))

        #officina
        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="sede"]')
        dropdown = Select(f_element)
        dropdown.select_by_index(13)
        time.sleep(0.1)

        #TRÁMITES POLICÍA NACIONAL
        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="tramiteGrupo[1]"]')
        dropdown = Select(f_element)
        dropdown.select_by_index(5)
        time.sleep(0.1)

        #ACEPTAR
        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnAceptar"]')
        actions.move_to_element(f_element).click().perform()

        time.sleep(randrange(4,7))

        #ENTRAR
        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnEntrar"]')
        actions.move_to_element(f_element).click().perform()

        time.sleep(2)

        # nie> pasaporte
        
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="comp04_id_citado"]/div[1]/fieldset/ul/li[2]/label')
        actions.move_to_element(f_element).click().perform()
        #pasport input

        PASSPORT= 'FV315480'
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="txtIdCitado"]')
        actions.move_to_element(f_element).click().perform()
        f_element.send_keys(str(PASSPORT))


        #Nombre y apellidos

        NOMYAPPE= 'Yevhen Maksymov'
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="txtDesCitado"]')
        actions.move_to_element(f_element).click().perform()
        f_element.send_keys(str(NOMYAPPE))

        # Año de nacimiento
        ANO='1991'
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="txtAnnoCitado"]')
        actions.move_to_element(f_element).click().perform()
        f_element.send_keys(str(ANO))

        #ACEPTAR


        f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnEnviar"]')
        actions.move_to_element(f_element).click().perform()
        time.sleep(randrange(2,5))
        
        #Solicitar cita
        if guard_blocking_states(driver):
            continue
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnEnviar"]')
        actions.move_to_element(f_element).click().perform()
        time.sleep(randrange(3,6))


        try:
            f_element=driver.find_element(By.XPATH, '//*[@id="mainWindow"]/div/div[2]/section/div[2]/form/div[1]/p')
            if f_element.text[:28] == 'En este momento no hay citas':        
                f_element = wait_clickable(driver,By.XPATH,'//*[@id="btnSalir"]')
                actions.move_to_element(f_element).click().perform()
        except NoSuchElementException:
        
            while True:
                pygame.mixer.init()
                sound = pygame.mixer.Sound('/home/yevhen/VScode/CITAS/ding-101492.mp3')
                sound.play()
                time.sleep(60)
                print("Что то нашел! проверь!")           


        time.sleep(randrange(90,95))   
