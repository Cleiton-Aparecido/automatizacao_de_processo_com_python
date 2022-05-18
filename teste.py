import pyautogui
import pyperclip
import pandas as pd
import time
from selenium import webdriver



navegador = webdriver.Chrome()
navegador.get("http://192.168.0.241/pos/indexDev.php")
org = navegador.find_element_by_xpath('//*[@id="salva_devolu"]/a[3]')


print("\n\n\nLink:",org.get_attribute("href"),"\n\n")