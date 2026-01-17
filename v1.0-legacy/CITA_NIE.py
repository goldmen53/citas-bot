from os import path
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
from main import enter_text, safe_wait_clickable, wait_clickable,guard_blocking_states,RestartLoop,click_button,click_dropdown



START_URL = 'https://icp.administracionelectronica.gob.es/icpco/index'
PASSPORT = 'FV315480'
NAME_SURNAME ='Yevhen Maksymov'
B_YEAR ='1991'
PROVINCIA=3 # 3 -ALICANTE
OFFICINA=13 # 13 -OEX ALICANTE, EBANISTERIA, 4-6, ALICANTE

TRIMINES_POLICIA=5 # 5 -POLICÍA - UCRANIA : SOLICITUD PROTECCIÓN TEMPORAL DESPLAZADOS


driver = Driver(uc=True)
driver.uc_open_with_reconnect(START_URL, 5)
actions = ActionChains(driver)
counter=0

while True:
    
    time.sleep(randrange(4,7))   
    counter+=1
    print(f'Количество попыток: {counter}') 

    if guard_blocking_states(driver,START_URL):
        continue
    try:
        f_element = wait_clickable(driver,By.XPATH,'//*[@id="cookie_action_close_header"]')
        actions.move_to_element(f_element).click().perform()
        time.sleep(0.1)
    except:
           pass
    
    
    if click_dropdown(actions,driver,'//*[@id="form"]',PROVINCIA):
        continue
    
    if click_button(actions,driver,'//*[@id="btnAceptar"]'):
        continue
    time.sleep(randrange(2,5))

    if click_dropdown(actions,driver,'//*[@id="sede"]',OFFICINA):
        continue
    if click_dropdown(actions,driver,'//*[@id="tramiteGrupo[1]"]',TRIMINES_POLICIA):
        continue
    time.sleep(0.1)

    if click_button(actions,driver,'//*[@id="btnAceptar"]'):
        continue
    time.sleep(randrange(2,4))

    if click_button(actions,driver,'//*[@id="btnEntrar"]'):
        continue
    time.sleep(2)

    if click_button(actions,driver,'//*[@id="comp04_id_citado"]/div[1]/fieldset/ul/li[2]/label'):
        continue

    enter_text(actions,driver,'//*[@id="txtIdCitado"]',PASSPORT)
    enter_text(actions,driver,'//*[@id="txtDesCitado"]',NAME_SURNAME)
    enter_text(actions,driver,'//*[@id="txtAnnoCitado"]',B_YEAR)

    if click_button(actions,driver,'//*[@id="btnEnviar"]'):
        continue
    time.sleep(randrange(2,3))

    if click_button(actions,driver,'//*[@id="btnEnviar"]'):
        continue
    

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
            
            print("Что то нашел! проверь!")
            time.sleep(60)             


    time.sleep(randrange(60,65))





