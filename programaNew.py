from __future__ import barry_as_FLUFL
from ast import Break
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
import PySimpleGUI as sg

def checkingLink(StatusLink):
    link = navegador.current_url
    contador = 0
    if(StatusLink == 'relacaoMudanca'):
        urlConf = "http://admin.boltcard.com.br/pos/cadastro/listar"
        if(link == urlConf):
            print('\n\nLink esta correto!!!\n\n')
        else:
            yzb = True
            while( yzb == True):
                contador = 1 + contador
                print('\n\nObtendo link correto',contador,'\n\n')
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3 ):
                    navegador.close()
                    os.system('cls')
                    yzb = False
                    print("Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif( link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    elif(StatusLink == 'relacaoConferencia'):
        urlConf = "http://admin.boltcard.com.br/pos/movimento/listar"
        if(link == urlConf):
            print('\n\nLink esta correto!!!\n\n')
        else:
            yzb = True
            while( yzb == True):
                contador = 1 + contador
                print('\n\nObtendo link correto',contador,'\n\n')
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3 ):
                    navegador.close()
                    os.system('cls')
                    yzb = False
                    print("Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif( link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    # elif(StatusLink == 'PosMudanca'):

def conferencia(config):
    url = "http://admin.boltcard.com.br/pos/movimento/listar"
    navegador.get(url)
    resultadoConf = []
    
    if(config == "mudanca"):
        print("\n\n__Iniciando conferencia para mudanca__\n\n")
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
                quit()
            else:
                print(
                    "\n\n\n\nContém pos em status configurado\nEquipamento esta configurado:", linha, "\n\n\n\n")
                navegador.close()
                quit()
            navegador.find_element_by_xpath(
                '//*[@id="dataTable_filter"]/label/input').clear()

    if(config == "insecao"):
        print("\n\n__Iniciando conferencia para alterar isenção__\n\n")
        for cont in range(qtdlinha):
            navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').click()
            pyperclip.copy(colunaSerial[cont])
            pyautogui.hotkey("ctrl", "v")
            conf = navegador.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr/td[11]').text
            colunaPdv[cont] = str(colunaPdv[cont])
            while(len(colunaPdv[cont]) < 6):
                colunaPdv[cont] = "0" + colunaPdv[cont]
            if(conf ==  colunaPdv[cont]):
                print("\n\nPDV esta correto com o sistema:",colunaPdv[cont],"\n\n")
            elif(conf != colunaPdv[cont]):
                resultadoConf.append(colunaSerial[cont]) 
            navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').clear()
        if(len( resultadoConf) == 0 ):
            print("Estão todas certas\n")
        else:
            navegador.close()
            os.system('cls')
            for i in range(len(resultadoConf)):
                print("O equipamento: ", resultadoConf[i],"Esta atrelado com o PDV divergente da planilha")
        
        

def conferenciaE():
    cont = 0
    print("\n\n__Iniciando conferencia estoque__\n\n")
    navegador.get("http://admin.boltcard.com.br/pos/movimento/listar")
    for linha in colunaSerial:
        navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(linha)
        pyautogui.hotkey("ctrl", "v")
        local = navegador.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr/td[7]').text
        time.sleep(0.2)
        print("\n\n\nStatus: ", local, " Numero de serie: ", linha, "\n\n\n")
        navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').clear()


def loginAdmin():
    url = "http://admin.boltcard.com.br/login"
    navegador.get(url)
    navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').click()
    pyperclip.copy(log)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("Tab")
    pyperclip.copy(senha)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("Enter")
    time.sleep(2)
   


def mudanca():
    loginAdmin()
    conferencia("mudanca")
    time.sleep(2)
    contd = 0
    for linha in range(qtdlinha):
        #------------------------#
        print("\n\n---mudando:", linha, "de ", qtdlinha, "---\n\n")
        url = "http://admin.boltcard.com.br/pos/cadastro/listar"
        navegador.get(url)
        print('\n\n\npassou pelo get\n\n\n')

        checkingLink('relacaoMudanca')

        print('\n\n\npassou pelo checking\n\n\n')
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(colunaSerial[linha])
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        navegador.find_element_by_xpath(
            '//*[@id="dataTable"]/tbody/tr/td[8]/a[1]').click()
        url = navegador.current_url
        navegador.get(url)
        navegador.find_element_by_xpath(
            '//*[@id="form_pos"]/div[1]/div[1]/div[6]/select').click()
        for es in colunaEstoque[linha]:
            pyautogui.hotkey(es)
        navegador.find_element_by_xpath('//*[@id="submeter"]').click()
    print("processo finalizado\nAguarde...")
    time.sleep(2)
    os.system('cls')
    conferenciaE()
    navegador.close()


def insecao():
    loginAdmin()
    conferencia("insecao")
    for a in range(qtdlinha):
        resultadoPorcentagem = (100*a)/qtdlinha
        os.system('cls')
        print("\n\n\nEm processo: ",resultadoPorcentagem,"%\n\n\n")
        navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(colunaSerial[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr/td[12]/a').click()
        navegador.get(navegador.current_url)
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
        time.sleep(1)
        navegador.find_element_by_xpath('//*[@id="dar_baixa_pos"]/div/div/form/div[2]/button[2]').click()
        time.sleep(1)
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/button').click()
        time.sleep(2)
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input').click()  
        pyperclip.copy(colunaPdv[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').clear()  
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').click()
        colunaValor[a] = str(colunaValor[a])
        colunaValor[a] = colunaValor[a] + "0"
        pyperclip.copy(colunaValor[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').clear()  
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').click()
        pyperclip.copy(x)
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]').click()
        # mudando para configurado
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a').click()
        url = navegador.current_url
        navegador.get(url)
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[3]/select').click()
        status = 'configuraco'
        for p in status:
            pyautogui.hotkey(p)
        navegador.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button').click()
        url = "http://admin.boltcard.com.br/pos/movimento/listar"
        navegador.get(url)
    navegador.close()    
    print("\n\n finalizado \n\n")    





#---principal---#

sg.theme('Dark') 
layout = [  [sg.Text('Login:'), sg.InputText()],
            [sg.Text('Senha:'), sg.InputText()],
            [sg.Button('Entrar'), sg.Button('Cancelar Programa')] ]
window = sg.Window('Login no Bolt Administrativo', layout)

event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancelar Programa': 
    window.close()
    sg.popup('Programa encerrando:')
    sg.popup('tchau...')
    window.close()
    quit()
    
window.close()
# log = input("Login com permissão: ")
# senha = input("senha: ")
log = values[0]
senha = values[1]
fechar = True

while fechar == True:
    cont = 0
    opcao = int(
        input('\n1 - mudança\n2 - registrar\n3 - finalizar\n4 - alterar isenção\n\n'))
    # opcao = 4
    if(opcao == 1):
        tabela = pd.read_excel('mudanca.xlsx')
        colunaSerial = tabela['Serial']
        colunaEstoque = tabela['Estoque']
        qtdlinha = tabela['Serial'].count()
        navegador = webdriver.Chrome()
        mudanca()
    elif(opcao == 2):
        print("registrar")
        fechar = False
    elif(opcao == 4):
        tabela = pd.read_excel('isencao.xlsx')
        colunaSerial = tabela['Serial']
        colunaPdv = tabela['pdv']
        colunaValor = tabela['valor']
        qtdlinha = tabela['Serial'].count()
        print("_______configurações da inseção_______\n")
        x = str(input("Data de inseção:"))
        # x = "01/05/2999"
        print("Data de inseção:",x,"\n\nTipo: ",type(x))
        navegador = webdriver.Chrome()
        navegadorPOS = navegador
        insecao()
    else:
        fechar = False
print("\n\n\n\n\n\n------------------------Finalizando sistma---------------------------\n\n\n\n\n\n")
