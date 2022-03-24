import pyautogui
import pyperclip
from selenium import webdriver  


#navegador = webdriver.Chrome()
#navegador.get("https://www.google.com.br")
#pyautogui.hotkey("ctrl","t")

print("Bem vindo ao programa de automatização\n\nDesenvolvido por Cleiton Ap. Bueno Fonseca\n\n");

opcao = int(input('Escolha uma opção: \n 1 - mudança\n2 - registrar\n'));


if opcao==1:
    print('mudança')
elif opcao==2:
    print("2")

else :
    print('registro')
