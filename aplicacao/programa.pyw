from ast import Str, Try
from cgi import print_directory
from dataclasses import asdict
from inspect import classify_class_attrs, isframe
from logging import _nameToLevel
from logging.handlers import TimedRotatingFileHandler
from operator import le
import os
from turtle import st
import pandas as pd
import time
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg
import re
import asyncio

#função para corrigir formatação da data
def inverterString(dataDesformatada):
    if type(dataDesformatada) ==  datetime:
        datastring = str(dataDesformatada)
        datastring = datastring[:10]
        data = datetime.strptime(datastring, '%Y-%m-%d').date()
        dataFormatada = data.strftime('%d/%m/%Y')
        datafinal = str(dataFormatada)
    elif type(dataDesformatada) == str:
        datafinal = dataDesformatada
    return datafinal

def login_macro():
    layout = [[sg.Text('Login:'), sg.InputText()],
            [sg.Text('Senha:'), sg.InputText(password_char='*')],
            [sg.Submit('Entrar'), sg.Button('Cancelar Programa')]]
    window = sg.Window('Login no Bolt Administrativo',layout,relative_location=(460,80))
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar Programa':
        window.close()
        sg.popup('Programa encerrado')
        window.close()
        quit()
    window.close() 
    return {"login":values[0],"senha":values[1]}

def loginAdmin(startlogin,login):
    url = "http://admin.boltcard.com.br/login"
    startlogin.get(url)
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[1]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[1]/input').send_keys(login['login'])
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[2]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[2]/input').send_keys(login['senha'])
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button')
    time.sleep(1)
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button').click()   

def login_tms7(nav,login):
    nav.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/Login.aspx")
    time.sleep(1)
    preencher_campo_xpath(nav,"/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[1]/input",login['login'])
    preencher_campo_xpath(nav,'/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[2]/input',login['senha'])
    clicar_xpath(navegador,'/html/body/div/div[2]/form/div[4]/fieldset/div[4]/input')

def print(texto):
    print = sg.Print
    print(texto,size=(40,20),relative_location=(530,-200))
    print("======================================|\n")

def Verificar_Render_xpath(nav,xpath):
    try:
        nav.find_element(By.XPATH,xpath)
        return True
    except :
        return False

def Verificar_Render_class(nav,classe):
    try:
        nav.find_element(By.CLASS_NAME,classe)
        return True
    except :
        return False

#funcao entrar no iframe
def entrar_iframe(nav,xpath_iframe):
    Aguardar_render_xpath(navegador,xpath_iframe)
    iframe = navegador.find_element(By.XPATH,xpath_iframe)
    nav.switch_to.frame(iframe)

#Função para verificar se o elemento xpath já esta carregado
def Aguardar_render_xpath(nav, xpathcode:str) -> None:
    WebDriverWait(nav, 10).until(EC.visibility_of_element_located((By.XPATH, xpathcode)))

def clicar_xpath(nav,xpath_pagina):
    # Aguardar_render_xpath(nav,xpath_pagina)
    time.sleep(2)
    nav.find_element(By.XPATH,xpath_pagina).click()

def preencher_campo_xpath(nav,xpath_pagina,conteudo):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).send_keys(str(conteudo))

def limpar_campo_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).clear()

def retornar_href_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    return  nav.find_element(By.XPATH,xpath_pagina).get_attribute("href")

def text_campo_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    return nav.find_element(By.XPATH,xpath_pagina).text

def lancar_cobranca_payware():
    tid_com_cobranca = []
    layout = [
                [sg.Text('Data de lancamento:'), sg.InputText()],
                [sg.Submit('Entrar'), sg.Button('Cancelar Programa')]]
    window = sg.Window('Data de lancamentos', layout,relative_location=(420,80))
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar Programa':
        window.close()
        sg.popup('Programa encerrado')
        window.close()
        quit()
    window.close()
    datalacamento = values[0]

    navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/loginUser.jsf?dswid=8086")
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[2]').send_keys(str(login_interface['login']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[3]').send_keys(str(login_interface['senha']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/div[1]/table/tbody/tr/td[1]/button/span').click()
    time.sleep(0.5)
    Aba_aberta = navegador.current_url
    navegador.get(Aba_aberta)   
    for cnpj_posicao in range(coluna_cnpj.count()):
        print("{} - Lancando cobranca no TID: {}\nCNPJ: {}\nValor: {}".format(cnpj_posicao+1,coluna_tid[cnpj_posicao],coluna_cnpj[cnpj_posicao],coluna_valor[cnpj_posicao]))
        navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/modules/acquirer/operationControl/templates/operationControlTemplate.jsf?openSearch=true&dswid=-7362")
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/ul/li[2]/a').click()
        navegador.get(navegador.current_url)   
        navegador.find_element(By.XPATH,'//*[@id="selectMerchantDocType_input"]').send_keys('1 - CNPJ')
        preencher_campo_xpath(navegador,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[2]/td[2]/input',coluna_cnpj[cnpj_posicao])
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td/button').click()
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[1]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]/div/ul/li[9]/a/span[2]')
        navegador.switch_to.default_content()   
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[2]')
        xpath_lista_comeco = '/html/body/div[4]/div[1]/div/div[1]/div/div/form/div[2]/div[3]/table/tbody/tr['
        xpath_lista_numero_tabela = 1
        xpath_lista_final = ']/td[1]'
        xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
        conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)   
        while conf_existencia_xpath_tabela == True:
            tid_retorno = navegador.find_element(By.XPATH,xpath).text
            # Verifica se existe o TID
            if coluna_tid[cnpj_posicao] == tid_retorno:
                clicar_xpath(navegador,xpath)
                time.sleep(4)
                clicar_xpath(navegador,'/html/body/div[4]/div[1]/ul/li[3]')
                # Confere se o TID foi encontrado com cobrança
                if navegador.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[3]/table/tbody/tr/td[1]").text != coluna_tid[cnpj_posicao]:
                    #na tela de serviços
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[6]/div/button[1]')
                    time.sleep(1.5)
                    preencher_campo_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[2]/div[2]/div/div/table/tbody/tr[4]/td[2]/div/div[2]/select',coluna_valor[cnpj_posicao])
                    time.sleep(0.5)
                    preencher_campo_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[2]/div[2]/div/div/table/tbody/tr[6]/td[2]/span/input',datalacamento)
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[2]/div[3]/span/button[1]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[6]/div/button[4]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[2]/div[3]/button[1]')
                    conf_existencia_xpath_tabela = False
                else: 
                    tid_com_cobranca.append({"tid":[coluna_tid[cnpj_posicao]],"cnpj":[coluna_cnpj[cnpj_posicao]]})
                    print("Já contem cobrança")      
            else: 
                xpath_lista_numero_tabela = xpath_lista_numero_tabela + 1
                xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
                conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)
    return tid_com_cobranca

def Excluir_Lancamentos_PayWare():
    navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/loginUser.jsf?dswid=8086")
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[2]').send_keys(str(login_interface['login']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[3]').send_keys(str(login_interface['senha']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/div[1]/table/tbody/tr/td[1]/button/span').click()
    time.sleep(0.5)
    Aba_aberta = navegador.current_url
    navegador.get(Aba_aberta)
    for cnpj_posicao in range(coluna_cnpj.count()):
        print("{} - Excluido TID {} do CNPJ {}".format(cnpj_posicao+1,coluna_tid[cnpj_posicao],coluna_cnpj[cnpj_posicao]))
        navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/modules/acquirer/operationControl/templates/operationControlTemplate.jsf?openSearch=true&dswid=-7362")
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/ul/li[2]/a').click()
        navegador.get(navegador.current_url)   
        navegador.find_element(By.XPATH,'//*[@id="selectMerchantDocType_input"]').send_keys('1 - CNPJ')
        preencher_campo_xpath(navegador,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[2]/td[2]/input',coluna_cnpj[cnpj_posicao])
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td/button').click()
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[1]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]/div/ul/li[9]/a/span[2]')
        navegador.switch_to.default_content()   
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[2]')
        xpath_lista_comeco = '/html/body/div[4]/div[1]/div/div[1]/div/div/form/div[2]/div[3]/table/tbody/tr['
        xpath_lista_numero_tabela = 1
        xpath_lista_final = ']/td[1]'
        xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
        conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)   
        while conf_existencia_xpath_tabela == True:
            tid_retorno = navegador.find_element(By.XPATH,xpath).text
            # Verifica se existe o TID
            if coluna_tid[cnpj_posicao] == tid_retorno:
                clicar_xpath(navegador,xpath)
                time.sleep(4)
                clicar_xpath(navegador,'/html/body/div[4]/div[1]/ul/li[3]')
                # Confere se o TID foi encontrado com cobrança
                if navegador.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[3]/table/tbody/tr/td[1]").text == coluna_tid[cnpj_posicao]:
                    #na tela de serviços
                    print("Contém cobrança!!!\nExcluindo")
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[3]/table/tbody/tr/td[1]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[6]/div/button[3]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[3]/div[3]/button[1]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,'/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[6]/div/button[4]')
                    time.sleep(0.5)
                    clicar_xpath(navegador,"/html/body/div[4]/div[2]/div[3]/button[1]")
                else: 
                    print("Sem Cobrança Lançada")      
            else: 
                xpath_lista_numero_tabela = xpath_lista_numero_tabela + 1
                xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
                conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)

        if conf_existencia_xpath_tabela == False:
            print("TID {} não encontrado".format(coluna_tid[cnpj_posicao]))
        
def conferencia_de_exclusao_lancamento_payware():
    lista_de_TID_com_cobranca_pos_exclusao = []
    print("INICIANDO CONFERENCIA DE EXCLUSAO")
    navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/loginUser.jsf?dswid=8086")
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[2]').send_keys(str(login_interface['login']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[3]').send_keys(str(login_interface['senha']))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/div[1]/table/tbody/tr/td[1]/button/span').click()
    time.sleep(0.5)
    Aba_aberta = navegador.current_url
    navegador.get(Aba_aberta)   
    for cnpj_posicao in range(coluna_cnpj.count()):
        print("{} - Conferindo TID {} do CNPJ {}".format(cnpj_posicao+1,coluna_tid[cnpj_posicao],coluna_cnpj[cnpj_posicao]))
        navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/modules/acquirer/operationControl/templates/operationControlTemplate.jsf?openSearch=true&dswid=-7362")
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/ul/li[2]/a').click()
        navegador.get(navegador.current_url)   
        navegador.find_element(By.XPATH,'//*[@id="selectMerchantDocType_input"]').send_keys('1 - CNPJ')
        preencher_campo_xpath(navegador,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[2]/td[2]/input',coluna_cnpj[cnpj_posicao])
        navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td/button').click()
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[1]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]')
        clicar_xpath(navegador,'/html/body/form/div/div[2]/div[3]/div/ul/li[9]/a/span[2]')
        navegador.switch_to.default_content()   
        entrar_iframe(navegador,'/html/body/div[6]/div/div/div[1]/iframe')
        entrar_iframe(navegador,'/html/frameset/frameset/frame[2]')
        xpath_lista_comeco = '/html/body/div[4]/div[1]/div/div[1]/div/div/form/div[2]/div[3]/table/tbody/tr['
        xpath_lista_numero_tabela = 1
        xpath_lista_final = ']/td[1]'
        xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
        conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)   
        while conf_existencia_xpath_tabela == True:
            tid_retorno = navegador.find_element(By.XPATH,xpath).text
            # Verifica se existe o TID
            if coluna_tid[cnpj_posicao] == tid_retorno:
                clicar_xpath(navegador,xpath)
                time.sleep(4)
                clicar_xpath(navegador,'/html/body/div[4]/div[1]/ul/li[3]')
                # Confere se o TID foi encontrado com cobrança
                if navegador.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div[3]/form/div[1]/div[3]/table/tbody/tr/td[1]").text == coluna_tid[cnpj_posicao]:
                    #na tela de serviços
                    print("Ainda contém cobrança no TID: {}".format(coluna_tid[cnpj_posicao]))
                    lista_de_TID_com_cobranca_pos_exclusao.append({"tid":[coluna_tid[cnpj_posicao]],"cnpj":[coluna_cnpj[cnpj_posicao]] })
                else: 
                    print("Sem Cobrança no TID: {}".format(coluna_tid[cnpj_posicao]))      
            else: 
                xpath_lista_numero_tabela = xpath_lista_numero_tabela + 1
                xpath = xpath_lista_comeco + str(xpath_lista_numero_tabela) + xpath_lista_final
                conf_existencia_xpath_tabela = Verificar_Render_xpath(navegador,xpath)
    return lista_de_TID_com_cobranca_pos_exclusao

def checkingLink(StatusLink):
    link = navegador.current_url
    contador = 0
    if(StatusLink == 'relacaoMudanca'):
        urlConf = "http://admin.boltcard.com.br/pos/cadastro/listar"
        if(link == urlConf):
            print('Verificado!')
        else:
            yzb = True
            while(yzb == True):
                contador = 1 + contador
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3):
                    navegador.close()
                    yzb = False
                    print("Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("Sistema estabilizado")
    elif(StatusLink == 'relacaoConferencia'):
        urlConf = "http://admin.boltcard.com.br/pos/movimento/listar"
        if(link == urlConf):
            print('Link esta correto!!!')
        else:
            yzb = True
            while(yzb == True):
                contador = 1 + contador
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3):
                    navegador.close()
                    yzb = False
                    print("Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("Sistema estabilizado")

def conferencia(config):
    confurl = navegador.current_url
    cont = 0
    url = "http://admin.boltcard.com.br/pos/movimento/listar"
    if(confurl != url):
        navegador.get(url)
    elif(confurl == url):
        print("link Ok")
    resultadoConfserial = []
    if(config == "mudanca"):
        print("__Iniciando conferencia para mudanca__")
        for linha in colunaSerial:
            cont += 1
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(linha)
            navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
            conf = navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[6]/span').text
            if conf == 'ESTOQUE':
                print("{} - Status: {} Numero de serie: {}".format(cont,conf,linha))
                retorno = True
            elif conf == '':
                sg.popup("\n Não exite numero de serie")
                quit()
            else:
                print("Contém pos em status configurado\nEquipamento esta configurado: {}".format(linha))
                sg.popup('Contém máquina de cartão\natrelado em pdv errado')
                navegador.close()
                retorno = False
                quit()

    if(config == "insecao"):
        print("__Iniciando conferencia para alterar isenção__")
        for cont in range(qtdlinha):
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(str(colunaSerial[cont]))
            navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
            conf = navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[11]').text
            colunaPdv[cont] = str(colunaPdv[cont])
            while(len(colunaPdv[cont]) < 6):
                colunaPdv[cont] = "0" + colunaPdv[cont]
            if(conf == colunaPdv[cont]):
                print("{} - PDV esta correto com o sistema: {}".format(cont+1,colunaPdv[cont]))
            elif(conf != colunaPdv[cont]):
                resultadoConfserial.append(colunaSerial[cont])
                print("{} - Divergência no sistema, PDV errado: {}".format(cont+1,colunaPdv[cont]))
        if(len(resultadoConfserial) == 0):
            print("Estão todas certas")
            retorno = True
        else:
            navegador.close()
            navegadorPOS.close()
            for i in range(len(resultadoConfserial)):
                print("O equipamento: {} Esta atrelado com o PDV divergente da planilha".format(resultadoConfserial[i]))
            print('Contém máquina de cartão\nAtrelado em pdv errado')
            sg.popup("Contém erros")
            retorno = False
    return retorno

def mudanca():
    print("Aguarde... Sistema Carregando...\nAbrindo 1° chrome ")
    loginAdmin(navegador,login_interface)
    print("Abrindo 2° chrome ")
    loginAdmin(navegadorPOS,login_interface)
    retorno = conferencia("mudanca")
    if retorno == True:
        for linha in range(qtdlinha):
            print("Alterando: {} de {},\nMudando POS:{} Para: {}.".format(linha + 1,qtdlinha,colunaSerial[linha],colunaEstoque[linha]))
            checkingLink('relacaoMudanca') #navegador
            limpar_campo_xpath(navegador,'//*[@id="dataTable_filter"]/label/input')
            preencher_campo_xpath(navegador,'//*[@id="dataTable_filter"]/label/input',colunaSerial[linha])
            urlAux = navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div/div/div/table/tbody/tr/td[8]/a[1]').get_attribute("href")
            navegadorPOS.get(urlAux)
            preencher_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[6]/select',colunaEstoque[linha])
            time.sleep(0.5)
            clicar_xpath(navegadorPOS,'//*[@id="submeter"]')
        print("Processo finalizado\nAguarde...")
    navegador.close()
    navegadorPOS.close()
    os.system('taskkill /f /im chromedriver.exe')

def insecao():
    layout = [[sg.Text('Data Isenção:'), sg.InputText()],
            [sg.Submit('Entrar'), sg.Button('Cancelar Programa')]]
    window = sg.Window('Data Isenção', layout,relative_location=(420,80))
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar Programa':
        window.close()
        sg.popup('Programa encerrado')
        window.close()
        quit()
    window.close()
    dataisencaomenu = values[0]
    print("Aguarde... Sistema Carregando...\nAbrindo 1° chrome ")
    loginAdmin(navegadorPOS,login_interface)
    print("Aguarde... Sistema Carregando...\nAbrindo 2° chrome ")
    loginAdmin(navegador,login_interface)
    retorno = conferencia("insecao")
    if retorno == True:
        print('passou    pela conferencia ')
        for a in range(qtdlinha):
            resultadoPorcentagem = (100*a)/qtdlinha
            print("Processo: {}%".format(resultadoPorcentagem))
            # buscar endereço para alteração
            limpar_campo_xpath(navegador,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input')
            preencher_campo_xpath(navegador,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input',colunaSerial[a])
            clicar_xpath(navegador,'//*[@id="btn_enviar"]')
            urlaux =  navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[12]/a').get_attribute("href")
            # Fim - buscar url   para alteração
            navegadorPOS.get(urlaux)
            clicar_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
            preencher_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[1]/div/div/div/select','bolt')
            clicar_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[2]/button[2]')
            navegadorPOS.get(urlaux)
            clicar_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
            #adicionar valores para configurar a pos com nova isenção
            colunaPdv[a] = str(colunaPdv[a])
            preencher_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input',colunaPdv[a])
            # formatar valor de isencao
            colunaValor[a] = str(colunaValor[a])
            colunaValor[a] = re.sub(r"[^a-zA-Z0-9]","",colunaValor[a])
            colunaValor[a] = colunaValor[a] + "0"
            #  Fim - formatar valor de isencao  
            limpar_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input')
            for adcValor in colunaValor[a]:
               preencher_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input',adcValor) 
            limpar_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input')
            for adcdata in dataisencaomenu:
                preencher_campo_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input',adcdata)     
            clicar_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]')
            #carrega a nova pagina com a isenção alterada
            urlaux = navegadorPOS.current_url
            navegadorPOS.get(urlaux)
            #pegar link para abrir nova aba para alterar a pos de correios para configurado  
            url_atualiza_status = retornar_href_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a') 
            #Abrir nova aba para alterar
            navegadorPOS.get(url_atualiza_status)
            preencher_campo_xpath(navegadorPOS,'//*[@id="form_pos"]/div[1]/div[1]/div[3]/select','CONFIGURADO')
            clicar_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button')
    navegador.close()
    navegadorPOS.close()
    os.system('taskkill /f /im chromedriver.exe')
    print("Finalizado")

def inserir_chip():
    print("Aguarde...\nAbrindo Chrome\n")
    print("Contém {} para registrar".format(colunaSerialChip.count()))
    loginAdmin(navegadorChip,login_interface)
    for qtd in range(colunaSerialChip.count()):
        navegadorChip.get('http://admin.boltcard.com.br/chip/home/inserir')
        print("{} - Número de serie: {},\npertencente a operadora {}.".format(qtd+1,colunaSerialChip[qtd],colunaOperadora[qtd]))
        Aguardar_render_xpath(navegadorChip,'//*[@id="form_pos"]/div[1]/div[1]/div[2]/input')
        navegadorChip.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[1]/div[2]/input').send_keys(str(colunaOperadora[qtd]))
        Aguardar_render_xpath(navegadorChip,'//*[@id="form_pos"]/div[1]/div[2]/div[2]/input')
        navegadorChip.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[2]/div[2]/input').send_keys(str(colunaSerialChip[qtd]))
        Aguardar_render_xpath(navegadorChip,'//*[@id="submeter"]')
        navegadorChip.find_element(By.XPATH,'//*[@id="submeter"]').click()   
    print("Finalizado...")
    navegadorChip.close()
    
def excluir_chip():
    print("Contém {} para registrar".format(colunaSerialChip.count()))
    print("Aguarde...\nAbrindo Chrome\n")
    loginAdmin(navegadorChip,login_interface)
    loginAdmin(navegador,login_interface)
    navegador.get("http://admin.boltcard.com.br/chip")
    for serial in colunaSerialChip:
        Aguardar_render_xpath(navegador,'//*[@id="dataTable_filter"]/label/input')
        navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').clear()
        navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').send_keys(str(serial))
        print("serial: {}".format(serial))
        if Verificar_Render_xpath(navegador,'//*[@id="dataTable"]/tbody/tr/td[6]/a'):
            AbaChip = navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[6]/a').get_attribute("href")
            navegadorChip.get(AbaChip)
            Aguardar_render_xpath(navegadorChip,'/html/body/div[2]/div[2]/main/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/a')
            navegadorChip.get(navegadorChip.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/a').get_attribute("href"))
            navegadorChip.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[3]/div/div/div/div/div/form/div/button').click()
            print("Excluído")
        else:
            print("Chip não Existe: {}".format(serial))
    
def excluir_tid_tms7():
    login_tms7(navegador,login_interface)
    navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/EstabelecimentosLista.aspx")
    for cont in range(tids.count()): 
        time.sleep(1)
        retorno_verificar_botao_pequisa = Verificar_Render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/p/span[1]')
        if retorno_verificar_botao_pequisa == False:
            login_tms7(navegador,login_interface)
            time.sleep(1)
            navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/EstabelecimentosLista.aspx")
        time.sleep(1) 
        clicar_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/p/span[1]')
        preencher_campo_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[1]/fieldset[2]/p[2]/input',tids[cont])
        clicar_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[2]/input')
        clicar_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[1]/div/table/tbody/tr[2]/td[3]')
        xpath_list_p_inicial = 'html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[1]/div/div/table/tbody/tr['
        xpath_list_p_number = 2
        xpath_list_p_final = ']/td[2]'
        xpath_list = xpath_list_p_inicial + str(xpath_list_p_number) + xpath_list_p_final
        tid_encontrado_na_lista = Verificar_Render_xpath(navegador,xpath_list)
        while tid_encontrado_na_lista == True:
            tid_retorno = navegador.find_element(By.XPATH,xpath_list).text  
            if tids[cont] == tid_retorno:
                print('{} - Tid encontrado\nTid encontrado: {}\nTid de buscar: {}\nTid sendo inativado...Aguarde'.format(cont+1,tid_retorno,tids[cont]))
                tid_encontrado_na_lista = False
                clicar_xpath(navegador,xpath_list)
                preencher_campo_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[2]/p[2]/select','Inativo')
                clicar_xpath(navegador,"/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[4]/input[4]")
                print("Tid inativado: {}".format(tids[cont]))
            else:
                xpath_list_p_number = int(xpath_list_p_number) + 1
                xpath_list = xpath_list_p_inicial + str(xpath_list_p_number) + xpath_list_p_final
                tid_encontrado_na_lista = Verificar_Render_xpath(navegador,xpath_list)
        navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/EstabelecimentosLista.aspx")      
    

#---principal---#
if __name__ == "__main__":
    sg.theme('Dark')
    print("Sistema Iniciado...")
    fechar = True

    while fechar == True:
        layout_menu = [
            [sg.Text('Menu de Seleção:\n',size=(30, 1), font='Lucida',justification='center',text_color="white",background_color="black")],
                [sg.Text("Funções BrasilCard - Admin",size=(30,1),font='Arial',justification="center")],
                [sg.Radio('Mudança de Estoque',"RADIO1", key='Mudanca')],
                [sg.Radio('Alterar isenção',"RADIO1", key='Alterar isenção')],
                [sg.Radio('Registrar Chip',"RADIO1", key='Registrar_Chip')],
                [sg.Radio('Excluir Chip',"RADIO1", key='exluir_Chip')],
                [sg.Text("Funcões PayWare",size= (30,1),font="Arial",justification="center")],
                [sg.Radio('Excluir Lançamentos PayWaye',"RADIO1", key='Excluir_Lancamentos_PayWare')],
                [sg.Radio('Lancar cobrança no PayWare',"RADIO1", key='Lancar_cobranca_PayWare')],
                [sg.Text("Funcões TMS - GER7",size=(30,1),font="Arial",justification="center")],
                [sg.Radio('Desativar TID TMS7',"RADIO1", key='inativar_tid_TMS7')],
                [sg.Submit('Processeguir'),sg.Button('Cancelar')]
        ]
        window_menu = sg.Window('Login no Bolt Administrativo', layout_menu)
        event, values = window_menu.read()
        window_menu.close()

        if(values['Mudanca'] == True):
            login_interface = login_macro()
            tabela = pd.read_excel('mudanca.xlsx')
            colunaSerial = tabela['Serial']
            colunaEstoque = tabela['Estoque']
            qtdlinha = tabela['Serial'].count()
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorPOS = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            navegadorPOS.minimize_window()
            mudanca()

        elif(values['Alterar isenção'] == True):
            login_interface = login_macro()
            tabela = pd.read_excel('isencao.xlsx')
            colunaSerial = tabela['Serial']
            colunaPdv = tabela['pdv']
            colunaValor = tabela['valor']
            qtdlinha = tabela['Serial'].count()
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorPOS = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            navegadorPOS.minimize_window()
            insecao()

        elif(values['Registrar_Chip'] == True):
            login_interface = login_macro()
            tabela = pd.read_excel('registrar-chip.xlsx')
            colunaSerialChip = tabela['serial_do_chip']
            colunaOperadora = tabela['operadora']
            qtdlinha = tabela['serial_do_chip'].count()
            navegadorChip = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorChip.minimize_window()
            inserir_chip()

        elif(values['exluir_Chip'] == True):
            login_interface = login_macro()
            tabela = pd.read_excel('excluir-chip.xlsx')
            colunaSerialChip = tabela['serial_do_chip']
            qtdlinha = tabela['serial_do_chip'].count()
            navegadorChip = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorChip.minimize_window()
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            excluir_chip()
            navegadorChip.close()
            navegador.close()

        elif(values['Excluir_Lancamentos_PayWare']):
            login_interface = login_macro()
            tabela = pd.read_excel('excluir_lancamentos_paywaye.xlsx')
            coluna_cnpj = tabela['CNPJ']
            coluna_tid = tabela['TID']
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            Excluir_Lancamentos_PayWare()
            navegador.close()
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            lista_TID_com_cobranca = conferencia_de_exclusao_lancamento_payware()
            if len(lista_TID_com_cobranca) > 0:
                print("Segue a quantidade de TID's que ainda contém cobranças: {}".format(len(lista_TID_com_cobranca)))
                for linha in lista_TID_com_cobranca:
                    print("CNPJ: {}\nTID: {}".format(linha['cnpj'],linha['tid']))
            else:
                print("Todos Tids Foram excluidos")
            navegador.close()
        
        elif(values['Lancar_cobranca_PayWare']):
            login_interface = login_macro()
            tabela = pd.read_excel('lancar_cobranca_paywaye.xlsx')
            coluna_cnpj = tabela['CNPJ']
            coluna_tid = tabela['TID']
            coluna_valor = tabela['VALOR']
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            lista_TID_com_cobranca = lancar_cobranca_payware()
            if len(lista_TID_com_cobranca) > 0:
                print("Cobranças lançadas\nPorém {} já haviam cobranças.\nSegue a lista abaixo:".format(len(lista_TID_com_cobranca)))
                for linha in lista_TID_com_cobranca:
                    print("CNPJ: {}\nTID: {}".format(linha['cnpj'],linha['tid']))
            else:
                print("Todas cobranças foram lançadas com sucesso")


        elif(values['inativar_tid_TMS7']):
            login_interface = login_macro()
            tabela = pd.read_excel('desativar_tid_tms7.xlsx')
            tids = tabela['TID']
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            excluir_tid_tms7()
            navegador.close()

        elif(values['Finalizar'] == True):
            fechar = False
            sg.popup('Programa encerrado')
            quit()

        else:
            fechar = False
            sg.popup('Programa encerrado')