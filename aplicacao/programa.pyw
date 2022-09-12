from ast import Str
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




def print(texto):
    print = sg.Print
    print(texto)
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")


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
                navegador.get(urlConf)
                link = navegador.current_url

                if(contador > 3):
                    navegador.close()
                    yzb = False
                    print("Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    elif(StatusLink == 'relacaoConferencia'):
        urlConf = "http://admin.boltcard.com.br/pos/movimento/listar"
        if(link == urlConf):
            print('\nLink esta correto!!!')
        else:
            yzb = True
            while(yzb == True):
                contador = 1 + contador
                print('\nObtendo link correto', contador)
                navegador.get(urlConf)
                link = navegador.current_url
                if(contador > 3):
                    navegador.close()
                    yzb = False
                    print( "Provavelmente o sistema Administrativo de POS esta offline, o programa será encerrado")
                    quit()
                elif(link == urlConf):
                    os.system('cls')
                    yzb = False
                    print("\n\nSistema estabilizado\n\n")
    # elif(StatusLink == 'PosMudanca'):
#Função para verificar se o elemento xpath esta na pagina
def chegarxpath(nav, xpathcode:str) -> None:
    WebDriverWait(nav, 60).until(EC.visibility_of_element_located((By.XPATH, xpathcode)))

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
        print("\n\n__Iniciando conferencia para mudanca__\n\n")
        for linha in colunaSerial:
            cont += 1
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(linha)
            navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
            conf = navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[6]/span').text
            if conf == 'ESTOQUE':
                print("\n",cont," - Status: ", conf, " Numero de serie: ", linha)
            elif conf == '':
                sg.popup("\n\n Não exite numero de serie")
                quit()
            else:
                print("\n\n\n\nContém pos em status configurado\nEquipamento esta configurado:", linha, "\n\n\n\n")
                sg.popup('Contém máquina de cartão\natrelado em pdv errado')
                navegador.close()
                quit()

    if(config == "insecao"):
        print("\n\n__Iniciando conferencia para alterar isenção__\n\n")
        for cont in range(qtdlinha):
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
            navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(colunaSerial[cont])
            navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
            conf = navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[11]').text

            colunaPdv[cont] = str(colunaPdv[cont])
            while(len(colunaPdv[cont]) < 6):
                colunaPdv[cont] = "0" + colunaPdv[cont]
            if(conf == colunaPdv[cont]):
                print("\n",cont+1," - PDV esta correto com o sistema:", colunaPdv[cont])
            elif(conf != colunaPdv[cont]):
                resultadoConfserial.append(colunaSerial[cont])
            
        if(len(resultadoConfserial) == 0):
            print("Estão todas certas\n")
        else:
            navegador.close()
            navegadorPOS.close()
            for i in range(len(resultadoConfserial)):
                print("\nO equipamento: ",resultadoConfserial[i], "Esta atrelado com o PDV divergente da planilha")
            sg.popup('Contém máquina de cartão\natrelado em pdv errado')
            quit()

def loginAdmin(startlogin):
    url = "http://admin.boltcard.com.br/login"
    startlogin.get(url)
    chegarxpath(startlogin,'/html/body/div[2]/div[2]/form/div[1]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[1]/input').send_keys(log)
    chegarxpath(startlogin,'/html/body/div[2]/div[2]/form/div[2]/input')
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[2]/input').send_keys(senha)
    chegarxpath(startlogin,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button')
    time.sleep(1)
    startlogin.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/div[3]/div/div[2]/button').click()   


def mudanca():
    print("Aguarde... Sistema Carregando...\nAbrindo 1° chrome ")
    loginAdmin(navegador)
    print("Abrindo 2° chrome ")
    loginAdmin(navegadorPOS)
    conferencia("mudanca")

    for linha in range(qtdlinha):
        print("\n---mudando:", linha + 1, "de ", qtdlinha, "---\nMudando:",
              colunaSerial[linha], " Para: ", colunaEstoque[linha], "\n")
        checkingLink('relacaoMudanca') #navegador
        navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').clear()
        colunaSerial[linha] = str(colunaSerial[linha])
        navegador.find_element(By.XPATH,'//*[@id="dataTable_filter"]/label/input').send_keys(colunaSerial[linha])
        urlAux = navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div/div/div/table/tbody/tr/td[8]/a[1]').get_attribute("href")
        navegadorPOS.get(urlAux)
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[6]/select')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/form/div[1]/div[1]/div[6]/select').send_keys(colunaEstoque[linha])
        chegarxpath(navegadorPOS,'//*[@id="submeter"]')
        time.sleep(0.5)
        navegadorPOS.find_element(By.XPATH,'//*[@id="submeter"]').click()
    print("processo finalizado\nAguarde...")
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
    print("\nAguarde... Sistema Carregando...\nAbrindo 2° chrome ")
    loginAdmin(navegador)
    conferencia("insecao")
    print('\n\n\npassou pela conferencia \n\n')
    for a in range(qtdlinha):
        resultadoPorcentagem = (100*a)/qtdlinha
        print("\nEm processo: ", resultadoPorcentagem, "%")
        checkingLink("insecao")

        # buscar endereço para alteração
        navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').clear()
        navegador.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[2]/div[1]/form/input').send_keys(colunaSerial[a])
        navegador.find_element(By.XPATH,'//*[@id="btn_enviar"]').click()
        urlaux =  navegador.find_element(By.XPATH,'//*[@id="dataTable"]/tbody/tr/td[12]/a').get_attribute("href")
        # Fim - buscar endereço para alteração

        navegadorPOS.get(urlaux)
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[1]/div/div/div/select')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[1]/div/div/div/select').send_keys('bolt')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[6]/div/div/form/div[2]/button[2]').click()
        navegadorPOS.get(urlaux)
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div/button').click()
                       
        # time.sleep(2)
        #adicionar valores para configurar a pos com nova isenção
        colunaPdv[a] = str(colunaPdv[a])
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[1]/div/div[1]/input').send_keys(colunaPdv[a])

        # formatar valor de isencao
        colunaValor[a] = str(colunaValor[a])
        colunaValor[a] = re.sub(r"[^a-zA-Z0-9]","",colunaValor[a])
        colunaValor[a] = colunaValor[a] + "0"
        #  Fim - formatar valor de isencao

        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').clear()
        for adcValor in colunaValor[a]:
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[3]/input').send_keys(adcValor)
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').clear()
        # datastring = inverterString(dataisencaomenu)
        for adcdata in dataisencaomenu:
            navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[1]/div/div/div[4]/input').send_keys(adcdata)
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[5]/div/div/form/div[2]/button[2]').click()
        #carrega a nova pagina com a isenção alterada
        urlaux = navegadorPOS.current_url
        navegadorPOS.get(urlaux)
        #pegar link para abrir nova aba para alterar a pos de correios para configurado
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a')
        url_atualiza_status = navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div/div/a').get_attribute("href")
        #Abrir nova aba para alterar
        navegadorPOS.get(url_atualiza_status)
        chegarxpath(navegadorPOS,'//*[@id="form_pos"]/div[1]/div[1]/div[3]/select')
        navegadorPOS.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[1]/div[3]/select').send_keys('CONFIGURADO')
        chegarxpath(navegadorPOS,'/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button')
        navegadorPOS.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/form/div[2]/button').click()   
    navegador.close()
    navegadorPOS.close()
    os.system('taskkill /f /im chromedriver.exe')
    print("\n\n finalizado \n\n")

def inserir_chip():
    print("Aguarde...\nAbrindo Chrome\n")
    loginAdmin(navegadorChip)
    for qtd in range(colunaSerialChip.count()):
        navegadorChip.get('http://admin.boltcard.com.br/chip/home/inserir')
        print("{} - Número de serie: {},\npertencente a operadora {}.\n".format(qtd+1,colunaSerialChip[qtd],colunaOperadora[qtd]))
        navegadorChip.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[1]/div[2]/input').send_keys(str(colunaOperadora[qtd]))
        navegadorChip.find_element(By.XPATH,'//*[@id="form_pos"]/div[1]/div[2]/div[2]/input').send_keys(str(colunaSerialChip[qtd]))
        navegadorChip.find_element(By.XPATH,'//*[@id="submeter"]').click()   
    print("\nFinalizado...")
    
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


    while fechar == True:
        cont = 0
        layout_menu = [[sg.Text('       Menu de Seleção\n\n1 - Mudança de Estoque\n2 - Alterar isenção\n3 - Registrar Chip\n4 - Excluir Chip\n0 - Finalizar')],
                    [
            sg.Radio(1, "RADIO1", key='Mudanca'),
            sg.Radio(2, "RADIO1", key='Alterar isenção'),
            sg.Radio(3, "RADIO1", key='Registrar_Chip'),
            sg.Radio(4, "RADIO1", key='exluit_Chip'),
            sg.Radio(0, "RADIO1", key='Finalizar')],
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
        elif(values['Registrar_Chip'] == True):
            tabela = pd.read_excel('registrar-chip.xlsx')
            colunaSerialChip = tabela['serial_do_chip']
            colunaOperadora = tabela['operadora']
            qtdlinha = tabela['serial_do_chip'].count()
            navegadorChip = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            navegadorChip.minimize_window()
            inserir_chip()
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
        elif(values['Finalizar'] == True):
            fechar = False
            sg.popup('Programa encerrado')
            quit()

        else:
            fechar = False
            sg.popup('Programa encerrado')

