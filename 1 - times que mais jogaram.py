import pandas as pd
import matplotlib.pyplot as plt

# Importando os dados da tabela do Excel
df = pd.read_excel('jogos.xlsx')

# Obtendo os times mais jogados
times_jogados = pd.concat([df['Time 1'], df['Time 2']]).value_counts()

# Gerando o gráfico de pizza com os times mais jogados
plt.figure(figsize=(8, 8))
plt.pie(times_jogados, labels=times_jogados.index, autopct='%1.1f%%', startangle=140)
plt.title('Times Que Mais Jogaram')
plt.axis('equal')
plt.show()
