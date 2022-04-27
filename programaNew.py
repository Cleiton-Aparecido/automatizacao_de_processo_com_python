from sqlite3 import Time
import pyautogui
import pyperclip
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os


def conferencia():
    cont = 0
    print("\n\n__Iniciando conferencia__\n\n")
    url = "http://admin.boltcard.com.br/pos/movimento/listar"
    navegador.get(url)
    for linha in colunaSerial:
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(linha)
        pyautogui.hotkey("ctrl", "v")
        conf = navegador.find_element_by_xpath(
            '//*[@id="dataTable"]/tbody/tr/td[6]').text
        time.sleep(0.2)

        if conf == 'ESTOQUE':
            print("Status: ", conf, " Numero de serie: ", linha)
        elif conf == '':
            print("\n\n Não exite numero de serie")
            break
        else:
            print(
                "\n\n\n\nContém pos em status configurado\nEquipamento esta configurado:", linha, "\n\n\n\n")
            navegador.close()
            break
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').clear()


def conferenciaE():
    cont = 0
    print("\n\n__Iniciando conferencia estoque__\n\n")
    navegador.get("http://admin.boltcard.com.br/pos/movimento/listar")
    for linha in colunaSerial:
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(linha)
        pyautogui.hotkey("ctrl", "v")
        local = navegador.find_element_by_xpath(
            '//*[@id="dataTable"]/tbody/tr/td[7]').text
        time.sleep(0.2)
        print("\n\n\nStatus: ", local, " Numero de serie: ", linha, "\n\n\n")
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').clear()


def loginAdmin():
    url = "http://admin.boltcard.com.br/login"
    navegador.get(url)
    navegador.find_element_by_xpath(
        '/html/body/div[2]/div[2]/form/div[1]/input').click()
    pyperclip.copy(log)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("Tab")
    pyperclip.copy(senha)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("Enter")
    time.sleep(2)
    # pyautogui.hotkey("Win", "left")
    # pyautogui.hotkey("Enter")
    # pyautogui.hotkey("Alt", "Tab")

def mudanca():
    loginAdmin()
    conferencia()
    time.sleep(2)
    contd = 0
    for linha in range(qtdlinha):
        #------------------------#
        print("\n\n---mudando:", linha, "de ", qtdlinha, "---\n\n")
        navegador.get("http://admin.boltcard.com.br/pos/cadastro/listar")
        navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(colunaSerial[linha])
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        navegador.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr/td[8]/a[1]').click()
        url = navegador.current_url
        navegador.get(url)
        navegador.find_element_by_xpath('//*[@id="form_pos"]/div[1]/div[1]/div[6]/select').click()
        for es in colunaEstoque[linha]:
            pyautogui.hotkey(es)
        navegador.find_element_by_xpath('//*[@id="submeter"]').click()
    print("processo finalizado\nAguarde...")
    time.sleep(2)
    os.system('cls')
    conferenciaE()
    navegador.close()


#---principal---#
fechar = True
# log = input("Login com permissão: ")
# senha = input("senha: ")
log = "cleiton"
senha = 123
# print("\n\n")
while fechar == True:
    tabela = pd.read_excel('mudanca.xlsx')
    colunaSerial = tabela['Serial']
    colunaEstoque = tabela['Estoque']
    qtdlinha = tabela['Serial'].count()
    cont = 0
    opcao = int( input('\n1 - mudança\n2 - registrar\n3 - finalizar\n4 - alterar isenção\n\n'))
    navegador = webdriver.Chrome()
    if(opcao == 1):
        mudanca()

    elif(opcao == 2):
        print("registrar")
        fechar = False
    else:
        fechar = False


print("\n\n\n\n\n\n------------------------Finalizando sistma---------------------------\n\n\n\n\n\n")
