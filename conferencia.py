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