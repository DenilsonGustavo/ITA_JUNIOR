from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

navegador.get("https://orteil.dashnet.org/cookieclicker/")

navegador.find_element('xpath', '/html/body/div[1]/div/a[1]').click()

navegador.find_element('xpath', '//*[@id="langSelect-PT-BR"]').click()

x=100
while(x>0):
    navegador.find_element('xpath', '//*[@id="bigCookie"]').click()
    x=x-1