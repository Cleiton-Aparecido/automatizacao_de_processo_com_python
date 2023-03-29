import click
import pyautogui
import pyperclip
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import date, datetime

datainicial = '9999-09-09 00:00:00'


datacortada = datainicial[:10]
datacortada = datetime(datacortada)

# data = datetime.strptime(datacortada, '%Y-%m-%D').date()


