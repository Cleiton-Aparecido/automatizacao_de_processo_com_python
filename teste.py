from lib2to3.pgen2 import driver
import pyautogui
import pyperclip
import time
from selenium import webdriver 
import pandas as pd
import os

url = "http://192.168.0.33/siweb_bolt/4420/public/login"
log = input("Login teste com permissão: ")
senha = input("senha teste:")
porta = input("Porta:")
navegador = webdriver.Chrome()
navegador.get(url)
pyautogui.hotkey('Win','Up')
navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').click()
pyperclip.copy(log)
pyautogui.hotkey("ctrl","v")
pyautogui.hotkey("Tab")
pyperclip.copy(senha)
pyautogui.hotkey("ctrl","v")
navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[3]/select').click()
for pt in porta:
     pyautogui.hotkey(pt)
navegador.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[4]/div/div[2]/button').click()

