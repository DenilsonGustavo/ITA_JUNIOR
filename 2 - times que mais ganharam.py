import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados da tabela do Excel
df = pd.read_excel('jogos.xlsx')

# Função para identificar o vencedor de cada partida
def identificar_vencedor(row):
    placar = row['Placar'].split(' - ')
    if int(placar[0]) > int(placar[1]):
        return row['Time 1']
    elif int(placar[0]) < int(placar[1]):
        return row['Time 2']
    else:
        return 'Empate'

# Criando uma nova coluna para armazenar o vencedor de cada partida
df['Vencedor'] = df.apply(identificar_vencedor, axis=1)

# Contando a quantidade de vitórias para cada time
times_vencedores = df['Vencedor'].value_counts()

# Gerando o gráfico de pizza com os times que mais ganharam
plt.figure(figsize=(8, 8))
plt.pie(times_vencedores, labels=times_vencedores.index, autopct='%1.1f%%', startangle=140)
plt.title('Porcentagem de vitória dos jogos')
plt.axis('equal')
plt.show()
