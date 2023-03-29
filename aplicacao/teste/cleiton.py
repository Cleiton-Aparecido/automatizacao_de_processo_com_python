from tokenize import Double3
import pyautogui
import pyperclip
from selenium import webdriver  


qtdlinha = 600
a = 1

resultadoPorcentagem = str((100*a)/qtdlinha)
print("\n Item:",a,", em processo: ", resultadoPorcentagem[0],resultadoPorcentagem[1],resultadoPorcentagem[2],resultadoPorcentagem[3], "%")