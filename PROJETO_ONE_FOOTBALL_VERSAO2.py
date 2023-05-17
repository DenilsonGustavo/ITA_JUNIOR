import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

time.sleep(2)
navegador.get("https://onefootball.com/pt-br/competicao/brasileirao-serie-a-16/resultados")
time.sleep(2)
link_http = navegador.current_url
headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
response = requests.get(link_http, headers=headers)
content = response.content
site = BeautifulSoup(content, 'html.parser')
#acoes = site.find('div', attrs={'class': 'Ovx(a) Ovx(h)--print Ovy(h) W(100%)'})
time.sleep(2)
#navegador.find_element('xpath', '/html/body/of-root/div/main/of-entity-stream/section/of-xpa-layout-entity/section[5]/of-xpa-switch-entity/section/of-match-cards-lists-appender/div/div/button').click()
#time.sleep(3)
url = navegador.current_url
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#Encontrar o campeonato
nome_campeonato = soup.find('p', class_='title-2-bold').get_text(strip=True)  # Obtém o nome do campeonato
wait = WebDriverWait(navegador, 10)
jogos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'simple-match-cards-list__match-card')))
lista_jogos = []
for i in range(len(jogos)):
    time.sleep(2)
    jogos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'simple-match-cards-list__match-card')))
    jogo = jogos[i]
    jogo.click()
    time.sleep(2)
    site = navegador.page_source
    s = BeautifulSoup(site, 'html.parser')
    jogo_encontrado = s.find('div', {'class': 'enforced-dark MatchScore_patternContainer__J7zzx'})
    team_elements = jogo_encontrado.find_all('span', class_='MatchScoreTeam_name__KtOJo MatchScoreTeam_titleStyle__PnSz6')
    info = s.find('ul', class_='MatchInfo_entries__lSpQD')
    Data = info.find_all('span', class_='title-8-regular MatchInfoEntry_subtitle__ntOIJ')
    dia = [element.get_text(strip=True) for element in Data]
    data = dia[1]
    status = jogo_encontrado.find('span', class_='title-8-medium')
    
    team_names = [element.get_text(strip=True) for element in team_elements]
    placar_div = jogo_encontrado.find('p', class_='MatchScore_scores__UWw03 title-2-bold')
    placar_texto = placar_div.get_text(strip=True)

    placar_time1, placar_time2 = placar_texto.split(':')
    
    team1_name = team_names[0]
    team2_name = team_names[1]

    score_team1 = placar_time1
    score_team2 = placar_time2
    
    #lista_jogadores = s.find('ul', class_='MatchEvents_matchEventsList__npzXI')
    #jogadores = lista_jogadores.find_all('li', class_='MatchEvents_matchEventsItem__AFOAF MatchEvents_matchEventsItemAway__TDngb')
    #jogadores_com_gol = [jogador for jogador in lista_jogadores if "Gol" in jogador]
    #jogo['Jogadores com Gol'] = jogadores_com_gol
    jogo = {'Campeonato': nome_campeonato, 'Time 1': team1_name, 'Time 2': team2_name, 'Placar': f'{score_team1} - {score_team2}'}
    
    if data:
        jogo['Data'] = data
    else:
        jogo['Data'] = ''

    if status:
        jogo['Status'] = status.get_text(strip=True)
    else:
        jogo['Status'] = ''
    # Adiciona o jogo à lista de jogos
    lista_jogos.append(jogo)
    
    print(f'Times: {team1_name} vs {team2_name}')
    print(f'Placar: {score_team1} - {score_team2}')
    print(f'Data: {data}')
    print(f'Status: {placar_texto}')
    print(f'Campeonato: {nome_campeonato}')
    navegador.back()

# Cria o dataframe com os jogos
df = pd.DataFrame(lista_jogos)

# Salva o dataframe em um arquivo Excel
df.to_excel('jogos_versao2.xlsx', index=False)