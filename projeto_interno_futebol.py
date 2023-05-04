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
navegador.get("https://www.espn.com.br/futebol/campeonatos")
time.sleep(2)
link_http = navegador.current_url

response = requests.get(link_http)
content = response.content
site = BeautifulSoup(content, 'html.parser')
acoes = site.find('div', attrs={'class': 'Ovx(a) Ovx(h)--print Ovy(h) W(100%)'})
time.sleep(2)
navegador.find_element('xpath', '//*[@id="fittPageContainer"]/div[3]/div/div/div/div[2]/div[2]/div/div[3]/div/section/div/a/h2').click()
time.sleep(3)
navegador.find_element('xpath', '//*[@id="global-nav-secondary"]/div/ul/li[3]/a/span[1]').click()
time.sleep(3)
navegador.find_element('xpath', '//*[@id="scoreboard-page"]/div[1]/div[2]/div/div/div[13]/a').click()
time.sleep(3)
url = navegador.current_url
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for day in range(7):
    time.sleep(5)
    date = '2023040' + str(day+1) if day+1 < 10 else '202304' + str(day+1)
    url_day = url + '/data/' + date
    response = requests.get(url_day)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    div_events = soup.find('div', {'id': 'events'})
    if div_events:
        divs = div_events.find_all('div')
        print(f'Número de elementos div dentro da div com o id "events" no dia {date}: {len(divs)}')
        if len(divs) != 0 :
            # Encontrar a tabela de jogos
            tabela_jogos = soup.find('table', class_='schedule has-team-logos align-left')
            if tabela_jogos:
                linhas_jogos = tabela_jogos.find_all('tr')
                for linha in linhas_jogos:
                    # Encontrar os times que se enfrentaram
                    times = linha.find_all('span', class_='team-name')
                    time_casa = times[0].text
                    time_fora = times[1].text
    
                    # Encontrar o placar final
                    placar = linha.find('td', class_='score').text
    
                     # Encontrar quem fez os gols
                    gols = linha.find_all('ul', class_='game-details')
                    gols_casa = gols[0].text
                    gols_fora = gols[1].text
    
                    # Encontrar a data do jogo
                    data_jogo = linha.find('td', class_='date-time').text
    
                    # Encontrar o campeonato
                    campeonato = linha.find('span', class_='league').text
    
                    print(f'{time_casa} {placar} {time_fora} - {data_jogo} - {campeonato}')
                    print(f'Gols Casa: {gols_casa}')
                    print(f'Gols Fora: {gols_fora}')