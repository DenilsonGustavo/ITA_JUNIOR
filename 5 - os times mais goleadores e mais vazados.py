import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados da tabela do Excel
df = pd.read_excel('jogos.xlsx')

# Dividindo a coluna 'Placar' em duas colunas separadas
df[['Gols Time 1', 'Gols Time 2']] = df['Placar'].str.split(' - ', expand=True).astype(int)

# Gráfico de barras para os times mais goleadores e mais vazados
gols_marcados = df.groupby('Time 1')['Gols Time 1'].sum().add(df.groupby('Time 2')['Gols Time 2'].sum(), fill_value=0)
gols_sofridos = df.groupby('Time 1')['Gols Time 2'].sum().add(df.groupby('Time 2')['Gols Time 1'].sum(), fill_value=0)

# Criando um novo DataFrame com os dados para o gráfico
data = pd.DataFrame({'Gols Marcados': gols_marcados, 'Gols Sofridos': gols_sofridos})
data.sort_values(by='Gols Marcados', inplace=True)

# Plotando o gráfico de barras
plt.figure(figsize=(10, 6))
data.plot.bar(color=['g', 'r'], alpha=0.7)
plt.title('Times Mais Goleadores e Mais Vazados')
plt.xlabel('Times')
plt.ylabel('Gols')
plt.legend()
plt.xticks(rotation=45)
plt.show()
