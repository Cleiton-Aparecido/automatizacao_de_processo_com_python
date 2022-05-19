# from __future__ import barry_as_FLUFL
# from ast import Break
# import os
import pyautogui
import pyperclip
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import PySimpleGUI as sg
print = sg.Print

def checkingLink(StatusLink):
    link = navegador.current_url
    contador = 0
    if(StatusLink == 'relacaoMudanca'):
        urlConf = "http://admin.boltcard.com.br/pos/cadastro/listar"
        if(link == urlConf):
            print('\n\nLink esta correto!!!\n\n')
        else:
            yzb = True
            while(yzb == True):
                contador = 1 + contador
                print('\n\nObtendo link correto', contador, '\n\n')
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3):
                    navegador.close()
                    os.system('cls')
                    yzb = False
                    print(
                        "Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    elif(StatusLink == 'relacaoConferencia'):
        urlConf = "http://admin.boltcard.com.br/pos/movimento/listar"
        if(link == urlConf):
            print('\n\nLink esta correto!!!\n\n')
        else:
            yzb = True
            while(yzb == True):
                contador = 1 + contador
                print('\n\nObtendo link correto', contador, '\n\n')
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3):
                    navegador.close()
                    os.system('cls')
                    yzb = False
                    print(
                        "Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    # elif(StatusLink == 'PosMudanca'):

def conferencia(config):
    confurl = navegador.current_url
    url = "http://admin.boltcard.com.br/pos/movimento/listar"
    if(confurl != url):
        navegador.get(url)
    elif(confurl == url):
        print("link Ok")
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
            navegador.find_element_by_xpath(
                '//*[@id="dataTable_filter"]/label/input').click()
            pyperclip.copy(colunaSerial[cont])
            pyautogui.hotkey("ctrl", "v")
            conf = navegador.find_element_by_xpath(
                '//*[@id="dataTable"]/tbody/tr/td[11]').text
            colunaPdv[cont] = str(colunaPdv[cont])
            while(len(colunaPdv[cont]) < 6):
                colunaPdv[cont] = "0" + colunaPdv[cont]
            if(conf == colunaPdv[cont]):
                print("\n\nPDV esta correto com o sistema:",
                      colunaPdv[cont], "\n\n")
            elif(conf != colunaPdv[cont]):
                resultadoConf.append(colunaSerial[cont])
            navegador.find_element_by_xpath(
                '//*[@id="dataTable_filter"]/label/input').clear()
        if(len(resultadoConf) == 0):
            print("Estão todas certas\n")
        else:
            navegador.close()
            os.system('cls')
            for i in range(len(resultadoConf)):
                print("O equipamento: ",
                      resultadoConf[i], "Esta atrelado com o PDV divergente da planilha")


def conferenciaE():
    cont = 0
    print("\n\n__Iniciando conferencia estoque__\n\n")
    navegador.get("http://admin.boltcard.com.br/pos/movimento/listar")
    cont = 0
    for linha in colunaSerial:
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(linha)
        pyautogui.hotkey("ctrl", "v")
        local = navegador.find_element_by_xpath(
            '//*[@id="dataTable"]/tbody/tr/td[7]').text
        time.sleep(0.2)
        print("\n\n\nEstoque pretentede: ",
              colunaEstoque[cont], "Estoque atual: ", local, " Numero de serie: ", linha, "\n\n\n")
        cont += 1
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').clear()


def loginAdmin():
    url = "http://admin.boltcard.com.br/login"
    navegador.get(url)
    navegador.maximize_window()
    navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').click()
    navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').send_keys(log)
    navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/input').send_keys(senha)
    navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button').click()   
    navegador.maximize_window()
    time.sleep(2)


def mudanca():
    loginAdmin()
    print("Aguarde... Sistema Carregando...")
    conferencia("mudanca")
    time.sleep(2)
    contd = 0
    for linha in range(qtdlinha):
        # sg.one_line_progress_meter('Em Processo', linha+1, qtdlinha, 'Em Processo','Aguarde a execução')
        #------------------------#
        print("\n\n---mudando:", linha, "de ", qtdlinha, "---\n\nMudando:",
              colunaSerial[linha], " Para: ", colunaEstoque[linha], "\n\n")
        url = "http://admin.boltcard.com.br/pos/cadastro/listar"
        navegador.get(url)
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        # pyperclip.copy(colunaSerial[linha])
        time.sleep(0.2)
        # pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath('//*[@id="dataTable_filter"]/label/input').send_keys(colunaSerial[linha])
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
        sg.one_line_progress_meter(
            'My Meter', a+1, qtdlinha, 'key', 'Optional message')
        resultadoPorcentagem = (100*a)/qtdlinha
        os.system('cls')
        print("\n\n\nEm processo: ", resultadoPorcentagem, "%\n\n\n")
        navegador.find_element_by_xpath(
            '//*[@id="dataTable_filter"]/label/input').click()
        pyperclip.copy(colunaSerial[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath(
            '//*[@id="dataTable"]/tbody/tr/td[12]/a').click()
        navegador.get(navegador.current_url)
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
        time.sleep(1)
        navegador.find_element_by_xpath(
            '//*[@id="dar_baixa_pos"]/div/div/form/div[2]/button[2]').click()
        time.sleep(1)
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/button').click()
        time.sleep(2)
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input').click()
        pyperclip.copy(colunaPdv[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').clear()
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').click()
        colunaValor[a] = str(colunaValor[a])
        colunaValor[a] = colunaValor[a] + "0"
        pyperclip.copy(colunaValor[a])
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').clear()
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').click()
        pyperclip.copy(x)
        pyautogui.hotkey("ctrl", "v")
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]').click()
        # mudando para configurado
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a').click()
        url = navegador.current_url
        navegador.get(url)
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[3]/select').click()
        status = 'configuraco'
        for p in status:
            pyautogui.hotkey(p)
        navegador.find_element_by_xpath(
            '/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button').click()
        url = "http://admin.boltcard.com.br/pos/movimento/listar"
        navegador.get(url)
    navegador.close()
    print("\n\n finalizado \n\n")


#---principal---#
sg.theme('Dark')
layout = [[sg.Text('Login:'), sg.InputText()],
          [sg.Text('Senha:'), sg.InputText(password_char='*')],
          [sg.Submit('Entrar'), sg.Button('Cancelar Programa')]]
window = sg.Window('Login no Bolt Administrativo', layout)

event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancelar Programa':
    window.close()
    sg.popup('Programa encerrado')
    window.close()
    quit()

window.close()
log = values[0]
senha = values[1]
fechar = True

while fechar == True:
    cont = 0
    layout_menu = [[sg.Text('\n1 - Mudança\n2 - Registrar\n3 - Alterar isenção\n0 - Finalizar')],
                   [
        sg.Radio(1, "RADIO1", key='Mudanca'),
        sg.Radio(2, "RADIO1", key='Registrar POS no sistema'),
        sg.Radio(3, "RADIO1", key='Alterar isenção'),
        sg.Radio(0, "RADIO1", key='Finalizar')],
        [sg.Submit('Processeguir')]
    ]
    window_menu = sg.Window('Login no Bolt Administrativo', layout_menu)
    event, values = window_menu.read()
    window_menu.close()
    if(values['Mudanca'] == True):
        tabela = pd.read_excel('mudanca.xlsx')
        colunaSerial = tabela['Serial']
        colunaEstoque = tabela['Estoque']
        qtdlinha = tabela['Serial'].count()
        navegador =webdriver.Chrome(executable_path=r'./chromedriver.exe')
        mudanca()
    elif(values['Registrar'] == True):
        print("registrar")
        fechar = False
    elif(values['Alterar isenção'] == True):
        tabela = pd.read_excel('isencao.xlsx')
        colunaSerial = tabela['Serial']
        colunaPdv = tabela['pdv']
        colunaValor = tabela['valor']
        qtdlinha = tabela['Serial'].count()
        layoutIsencaoP2 = [[sg.Text('Data da isenção:'), sg.InputText(key='DataIsencao')],
                           [sg.Submit('Processeguir')]]
        WindowLayoutIsencao = sg.Window(
            'Escolha a data de isenção', layoutIsencaoP2)
        evento, valor = WindowLayoutIsencao.read()
        navegador =webdriver.Chrome(executable_path=r'./chromedriver.exe')
        navegadorPOS = navegador
        insecao()
    elif(values['Finalizar'] == True):
        fechar = False
        sg.popup('Programa encerrado')
        quit()

    else:
        fechar = False
        sg.popup('Programa encerrado')

