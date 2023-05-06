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
time.sleep(8)
navegador.find_element('xpath', '//*[@id="scoreboard-page"]/div[1]/div[2]/div/div/div[13]/a').click()
time.sleep(8)
url = navegador.current_url
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
dados = []
#Encontrar o campeonato
header = soup.find('header', {'class': 'automated-header'})
campeonato = header.find('h1').text if header else None
for day in range(7):
    time.sleep(3)
    timeA = '-'
    timeB = '-'
    gols_de_A = '0'
    gols_de_B = '0'
    time.sleep(2)
    date = '2023040' + str(day+1) if day+1 < 10 else '202304' + str(day+1)
    url_day = url + '/data/' + date
    response = requests.get(url_day)
    soup = BeautifulSoup(response.content, 'html.parser')
    jogos = soup.find('div', {'id': 'events'})
    jogos_encontrados = jogos.find_all('article', {'class': 'scoreboard soccer fallback js-show'})
    quantidade_jogos = len(jogos_encontrados)
    if quantidade_jogos != 0 :
        # Encontrar a tabela de jogos
        jogos = soup.find('div', {'id': 'events'})
        if len(jogos)!=0:
            jogos_encontrados = jogos.find_all('article', {'class': 'scoreboard soccer fallback js-show'})
            for jogo_encontrado in jogos_encontrados:
                competitors =  jogo_encontrado.find('div', {'class': 'competitors'})
                #Encontrar os times que se enfrentaram
                #TIME A
                #Nome de A
                team_a = competitors.find('div', {'class': ['team', 'team-a']})
                short_name = team_a.find('span', {'class': 'short-name'})
                if short_name is not None:
                    timeA = short_name.text
                #gols do time A
                score_container = team_a.find('div', {'class': 'score-container'})
                if score_container is not None:
                    score = score_container.find('span', {'class': 'score'})
                    if score is not None:    
                        gols_de_A = score.text
                #Encontrar quem fez os gols
                nomes_dos_jogadoresA = []
                for jogo_encontrado in jogos_encontrados:
                    team_info = team_a.find('div', {'class': ['team-info', 'players']})
                    jogadores = team_info.find_all('li')
                    for jogador in jogadores:
                        nome_do_jogador = jogador.text
                        nomes_dos_jogadoresA.append(nome_do_jogador)
                
                #TIME B
                #Nome de B
                team_b = competitors.find('div', {'class': ['team', 'team-b']})
                short_name = team_b.find('span', {'class': 'short-name'})
                if short_name is not None:
                    timeB = short_name.text
                #gols do time B
                score_container = team_b.find('div', {'class': 'score-container'})
                if score_container is not None:
                    score = score_container.find('span', {'class': 'score'})
                    if score is not None:
                        gols_de_B = score.text
                #Encontrar quem fez os gols
                nomes_dos_jogadoresB = []
                for jogo_encontrado in jogos_encontrados:
                    team_info = team_b.find('div', {'class': ['team-info', 'players']})
                    jogadores = team_info.find_all('li')
                    for jogador in jogadores:
                        nome_do_jogador = jogador.text
                        nomes_dos_jogadoresB.append(nome_do_jogador)

                #Tempo de jogo
                game_status = jogo_encontrado.find('div', {'class': 'game-status'})
                if game_status is not None:
                    game_time = game_status.find('span', {'class': 'game-time'})
                    if game_time is not None:
                        tempo_do_jogo = game_time.text
                dados.append({'Campeonato': campeonato, 'Data': date, 'Time A': timeA, 'Time B': timeB, 'Placar': gols_de_A+'VS'+ gols_de_B,'Gols de A':nomes_dos_jogadoresA,'Gols de B': nomes_dos_jogadoresB})
df = pd.DataFrame(dados)
df.to_excel('meus_dados.xlsx', index=False)