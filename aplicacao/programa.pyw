from ast import Str, Try
from dataclasses import asdict
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
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg
import re
import asyncio




def print(texto):
    print = sg.Print
    print(texto)
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n")

def Verificar_Render_xpath(nav,xpath):
    try:
        nav.find_element(By.XPATH,xpath)
        return True
    except :
        return False

def clicar_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).click()

def preenchar_campo_xpath(nav,xpath_pagina,conteudo):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).send_keys(str(conteudo))

def limpar_campo_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).clear()

def href_campo_xpath(nav,xpath_pagina):
    Aguardar_render_xpath(nav,xpath_pagina)
    nav.find_element(By.XPATH,xpath_pagina).get_attribute("href")

#Função para verificar se o elemento xpath esta na pagina
def Aguardar_render_xpath(nav, xpathcode:str) -> None:
    WebDriverWait(nav, 60).until(EC.visibility_of_element_located((By.XPATH, xpathcode)))


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

def loginAdmin(startlogin):
    url = "http://admin.boltcard.com.br/login"
    startlogin.get(url)
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[1]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[1]/input').send_keys(log)
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[2]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[2]/input').send_keys(senha)
    Aguardar_render_xpath(startlogin,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button')
    time.sleep(1)
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button').click()   


def mudanca():
    print("Aguarde... Sistema Carregando...\nAbrindo 1° chrome ")
    loginAdmin(navegador)
    print("Abrindo 2° chrome ")
    loginAdmin(navegadorPOS)
    retorno = conferencia("mudanca")
    if retorno == True:
        for linha in range(qtdlinha):
            print("Alterando: {} de {},\nMudando POS:{} Para: {}.".format(linha + 1,qtdlinha,colunaSerial[linha],colunaEstoque[linha]))
            checkingLink('relacaoMudanca') #navegador
            navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').clear()
            colunaSerial[linha] = str(colunaSerial[linha])
            navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').send_keys(colunaSerial[linha])
            urlAux = navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div/div/div/table/tbody/tr/td[8]/a[1]').get_attribute("href")
            navegadorPOS.get(urlAux)
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[6]/select')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[6]/select').send_keys(colunaEstoque[linha])
            Aguardar_render_xpath(navegadorPOS,'//*[@id="submeter"]')
            time.sleep(0.5)
            navegadorPOS.find_element(By.XPATH,'//*[@id="submeter"]').click()
        print("Processo finalizado\nAguarde...")
    navegador.close()
    navegadorPOS.close()
    os.system('taskkill /f /im chromedriver.exe')



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


def insecao():
    layout = [[sg.Text('Data Isenção:'), sg.InputText()],
            [sg.Submit('Entrar'), sg.Button('Cancelar Programa')]]
    window = sg.Window('Data Isenção', layout)

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancelar Programa':
        window.close()
        sg.popup('Programa encerrado')
        window.close()
        quit()

    window.close()
    dataisencaomenu = values[0]
   

    print("Aguarde... Sistema Carregando...\nAbrindo 1° chrome ")
    loginAdmin(navegadorPOS)
    print("Aguarde... Sistema Carregando...\nAbrindo 2° chrome ")
    loginAdmin(navegador)
    retorno = conferencia("insecao")
    if retorno == True:
        print('passou    pela conferencia ')
        for a in range(qtdlinha):
            resultadoPorcentagem = (100*a)/qtdlinha
            print("Processo: {}%".format(resultadoPorcentagem))

            # buscar endereço para alteração
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(str(colunaSerial[a]))
            navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
            urlaux =  navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[12]/a').get_attribute("href")
        
            # Fim - buscar url   para alteração
            navegadorPOS.get(urlaux)
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[1]/div/div/div/select')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[1]/div/div/div/select').send_keys('bolt')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[2]/button[2]').click()
            navegadorPOS.get(urlaux)
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
                        
            #adicionar valores para configurar a pos com nova isenção
            colunaPdv[a] = str(colunaPdv[a])
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input').send_keys(colunaPdv[a])

            # formatar valor de isencao
            colunaValor[a] = str(colunaValor[a])
            colunaValor[a] = re.sub(r"[^a-zA-Z0-9]","",colunaValor[a])
            colunaValor[a] = colunaValor[a] + "0"
            #  Fim - formatar valor de isencao

            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').clear()
            for adcValor in colunaValor[a]:
                navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').send_keys(adcValor)
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').clear()
            # datastring = inverterString(dataisencaomenu)
            for adcdata in dataisencaomenu:
                navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').send_keys(adcdata)
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]').click()
            #carrega a nova pagina com a isenção alterada
            urlaux = navegadorPOS.current_url
            navegadorPOS.get(urlaux)
            #pegar link para abrir nova aba para alterar a pos de correios para configurado
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a')
            url_atualiza_status = navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a').get_attribute("href")
            #Abrir nova aba para alterar
            navegadorPOS.get(url_atualiza_status)
            Aguardar_render_xpath(navegadorPOS,'//*[@id="form_pos"]/div[1]/div[1]/div[3]/select')
            navegadorPOS.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[1]/div[3]/select').send_keys('CONFIGURADO')
            Aguardar_render_xpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button')
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button').click()   
    navegador.close()
    navegadorPOS.close()
    os.system('taskkill /f /im chromedriver.exe')
    print("Finalizado")

def inserir_chip():
    print("Aguarde...\nAbrindo Chrome\n")
    print("Contém {} para registrar".format(colunaSerialChip.count()))
    loginAdmin(navegadorChip)
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
    loginAdmin(navegadorChip)
    loginAdmin(navegador)
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
    
def Excluir_Lancamentos_PayWare():
    navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/loginUser.jsf?dswid=8086")
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[2]').send_keys(str(log))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/input[3]').send_keys(str(senha))
    navegador.find_element(By.XPATH,'/html/body/div[3]/div/div/form/div[1]/table/tbody/tr/td[1]/button/span').click()
    time.sleep(0.5)
    Aba_aberta = navegador.current_url
    navegador.get(Aba_aberta)   
    navegador.get("https://cardsutility.br.eds.com/CMS-ACQUIRER/modules/acquirer/operationControl/templates/operationControlTemplate.jsf?openSearch=true&dswid=-7362")
    navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/ul/li[2]/a').click()
    navegador.get(navegador.current_url)   
    navegador.find_element(By.XPATH,'//*[@id="selectMerchantDocType_input"]').send_keys('1 - CNPJ')
    navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[2]/td[2]/input').send_keys('38659839000109')
    navegador.find_element(By.XPATH,'/html/body/div[6]/div/div/div/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td/button').click()
    time.sleep(5)
    navegador.get(navegador.current_url) 
    
    navegador.find_element(By.XPATH,'/html/body/form/div/div[2]/div[3]/div/ul/li[9]/a/span[2]').click()
    # x = Verificar_Render_xpath(navegador,"/html/body/form/div/div[2]/div[3]")
    # print("retorno do botão: {}".format(x))



def excluir_tid_tms7():
    login_tms7()

    for cont in range(tids.count()):
        navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/EstabelecimentosLista.aspx")
        retorno_verificar_botao_pequisa = Verificar_Render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/p/span[1]')
        print("retorno do login: {}".format(retorno_verificar_botao_pequisa))

        if retorno_verificar_botao_pequisa == False:
            login_tms7()
            navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/EstabelecimentosLista.aspx")
        Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/p/span[1]')
        navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/p/span[1]').click()  
        Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[1]/fieldset[2]/p[2]/input')
        navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[1]/fieldset[2]/p[2]/input').send_keys(str(tids[cont]))
        Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[2]/input')
        navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/fieldset/div[2]/input').click()
        Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[1]/div/table/tbody/tr[2]/td[3]')
        navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[1]/div/table/tbody/tr[2]/td[3]').click()

        xpath_list_p_inicial = 'html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[1]/div/div/table/tbody/tr['
        xpath_list_p_number = 2
        xpath_list_p_final = ']/td[2]'

        xpath_list = xpath_list_p_inicial + str(xpath_list_p_number) + xpath_list_p_final

        tid_encontrado_na_lista = Verificar_Render_xpath(navegador,xpath_list)

        while tid_encontrado_na_lista == True:
        
            tid_retorno = navegador.find_element(By.XPATH,xpath_list).text
            
            if tid_encontrado(tids[cont],tid_retorno):
                print('{} - Tid encontrado\nTid encontrado: {}\nTid de buscar: {}\nTid sendo inativado...Aguarde'.format(cont+1,tid_retorno,tids[cont]))
                tid_encontrado_na_lista = False
                Aguardar_render_xpath(navegador,xpath_list)
                navegador.find_element(By.XPATH,xpath_list).click()
                Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[2]/p[2]/select')
                navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[2]/p[2]/select').send_keys('Inativo')
                Aguardar_render_xpath(navegador,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[4]/input[4]')
                navegador.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[4]/fieldset/div[7]/div[4]/input[4]').click()
                print("Tid inativado: {}".format(tids[cont]))
            else:
                xpath_list_p_number = int(xpath_list_p_number) + 1
                xpath_list = xpath_list_p_inicial + str(xpath_list_p_number) + xpath_list_p_final
                tid_encontrado_na_lista = Verificar_Render_xpath(navegador,xpath_list)

def login_tms7():

    navegador.get("https://app.ger7.com.br/TMS7/BoltCardProd/Pages/Login.aspx")

    Aguardar_render_xpath(navegador,'/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[1]/input')
    navegador.find_element(By.XPATH,'/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[1]/input').send_keys(str(log))
    Aguardar_render_xpath(navegador,'/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[2]/input')
    navegador.find_element(By.XPATH,'/html/body/div/div[2]/form/div[4]/fieldset/div[1]/p[2]/input').send_keys(str(senha))
    Aguardar_render_xpath(navegador,'/html/body/div/div[2]/form/div[4]/fieldset/div[4]/input')
    navegador.find_element(By.XPATH,'/html/body/div/div[2]/form/div[4]/fieldset/div[4]/input').click()  

def tid_encontrado(tid_buscar,tid_retorno):
    if tid_retorno == tid_buscar:
        return True
    else:
        return False



#---principal---#
if __name__ == "__main__":

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

    print("Sistema Iniciado...")
    while fechar == True:
        cont = 0
        layout_menu = [[sg.Text('Menu de Seleção\n\n1 - Mudança de Estoque\n2 - Alterar isenção\n3 - Registrar Chip\n4 - Excluir Chip\n5 - Excluir Lançamentos PayWaye\n6 - Desativar TID TMS7\n0 - Finalizar')],
                    [
                sg.Radio(1,"RADIO1", key='Mudanca'),
                sg.Radio(2,"RADIO1", key='Alterar isenção'),
                sg.Radio(3,"RADIO1", key='Registrar_Chip'),
                sg.Radio(4,"RADIO1", key='exluir_Chip'),
                sg.Radio(5,"RADIO1", key='Excluir_Lancamentos_PayWare'),
                sg.Radio(6,"RADIO1", key='inativar_tid_TMS7'),
                sg.Radio(0,"RADIO1", key='Finalizar')
            ],
            [sg.Submit('Processeguir'),sg.Button('Cancelar')]
        ]
        window_menu = sg.Window('Login no Bolt Administrativo', layout_menu)
        event, values = window_menu.read()
        window_menu.close()

        if(values['Mudanca'] == True):
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
            tabela = pd.read_excel('registrar-chip.xlsx')
            colunaSerialChip = tabela['serial_do_chip']
            colunaOperadora = tabela['operadora']
            qtdlinha = tabela['serial_do_chip'].count()
            navegadorChip = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorChip.minimize_window()
            inserir_chip()
        elif(values['exluir_Chip'] == True):
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
            tabela = pd.read_excel('excluir_lancamentos_paywaye.xlsx')
            coluna_cnpj = tabela['CNPJ']
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegador.minimize_window()
            # Excluir_Lancamentos_PayWare()
            navegador.close()

        elif(values['inativar_tid_TMS7']):
            tabela = pd.read_excel('desativar_tid_tms7.xlsx')
            tids = tabela['TID']
            navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            # navegador.minimize_window()
            excluir_tid_tms7()

        elif(values['Finalizar'] == True):
            fechar = False
            sg.popup('Programa encerrado')
            quit()
        else:
            fechar = False
            sg.popup('Programa encerrado')

