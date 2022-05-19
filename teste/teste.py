import click
import pyautogui
import pyperclip
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By



navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe')
navegador.get("http://192.168.0.241/pos/indexDev.php")
org = navegador.find_element_by_xpath('//*[@id="salva_devolu"]/a[3]')
urlAux = navegador.find_element_by_xpath('//*[@id="salva_devolu"]/a[3]').get_attribute("href")

# print("\n\n\nLink:",org.get_attribute("href"),"\n\n")

webdriver.ActionChains(navegador).key_down(Keys.CONTROL).click(org).perform()
navegador.find_element_by_tag_name(org).send_keys(Keys.CONTROL + 't') 

print("passou")

