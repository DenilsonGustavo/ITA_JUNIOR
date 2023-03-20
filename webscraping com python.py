import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

time.sleep(2)
navegador.get("https://us.yahoo.com/")
time.sleep(2)
navegador.find_element('xpath', '//*[@id="root_3"]').click()
time.sleep(3)
navegador.find_element('xpath', '//*[@id="data-util-col"]/section[5]/header/a').click()

#------------------------------------------------------------------------------
time.sleep(3)

link_http = navegador.current_url

response = requests.get(link_http)
content = response.content
site = BeautifulSoup(content, 'html.parser')
acoes = site.find('div', attrs={'class': 'Ovx(a) Ovx(h)--print Ovy(h) W(100%)'})
time.sleep(2)

print(acoes)

simbolos = site.findAll('td', attrs={'aria-label': 'Symbol'})
nomes = site.findAll('td', attrs={'aria-label': 'Name'})
variacoes_porcentagem = site.findAll('td', attrs={'aria-label': '% Change'})
variacoes_nominais = site.findAll('td', attrs={'aria-label': 'Change'})
volumes = site.findAll('td', attrs={'aria-label': 'Volume'})
valores_mercado = site.findAll('td', attrs={'aria-label': 'Market Cap'})

lista_acoes = []
for simbolo, nome, variacao_porcentagem, variacao_nominal, volume, valor_mercado  in zip(simbolos, nomes, 
                                                                                                   variacoes_porcentagem,
                                                                                                  variacoes_nominais,
                                                                                                  volumes, valores_mercado):

    #print(simbolo.text, nome.text, variacao_porcentagem.text, variacao_nominal.text, volume.text, valor_mercado.text)
    lista_acoes.append([simbolo.text, nome.text, variacao_porcentagem.text, variacao_nominal.text, volume.text, valor_mercado.text])
Acoes_planilha = pd.DataFrame(lista_acoes, columns=["Sigla","Nome","Variação em %","Variação","Volume","Valor de Mercado"])
print(Acoes_planilha)
Acoes_planilha.to_excel('Acoes_Planilha.xlsx', index=False)