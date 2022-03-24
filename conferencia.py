from lib2to3.pgen2 import driver
import pyautogui
import pyperclip
import time
from selenium import webdriver 
import pandas as pd
import os

navegador = webdriver.Chrome()
url = "http://admin.boltcard.com.br/login"
navegador.get(url)
pyautogui.hotkey('Win','Up')
navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').click()
teste = 'cleiton'
pyperclip.copy(teste)
pyautogui.hotkey("ctrl","v")
pyautogui.hotkey("Tab")
pyperclip.copy("123")
pyautogui.hotkey("ctrl","v")
pyautogui.hotkey("Enter")
#conferencia
url = navegador.current_url
navegador.get(url)
tabela = pd.read_excel('mudanca.xlsx')
colunaSerial = tabela['Serial']
for linha in colunaSerial:
    navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').click()
    pyperclip.copy(linha)
    pyautogui.hotkey("ctrl","v")
    conf = navegador.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr/td[6]').text
    
    if conf == 'ESTOQUE':
        print("Estoque: ",conf," Numero de serie: ",linha)
    else:
        print("\n\n\n\nContém pos em status configurado\nEquipamento esta configurado: ",linha)
        navegador.close()
        break
    navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').clear()
navegador.close()
print("finalizar")
        