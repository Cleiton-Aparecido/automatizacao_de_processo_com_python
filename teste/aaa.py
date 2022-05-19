from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome(executable_path=r'../chromedriver.exe')

# Navigate to url
driver.get("http://www.google.com")

# Store 'google search' button web element
searchBtn = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div[2]/a')

# Perform context-click action on the element

webdriver.ActionChains(driver).key_down(Keys.CONTROL).click(searchBtn).perform()

# webdriver.ActionChains(driver).key_down(Keys.CONTROL).perform()