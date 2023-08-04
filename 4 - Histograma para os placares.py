import pandas as pd
import matplotlib.pyplot as plt

# Importing data from the Excel table
df = pd.read_excel('jogos.xlsx')

# Histogram for scores
df['Placar'] = df['Placar'].apply(lambda x: sum(map(int, x.split(' - '))))

# Counting the number of games for each total number of goals
data = df['Placar'].value_counts().sort_index()

# Plotting the horizontal bar chart
plt.figure(figsize=(8, 6))
data.plot.barh(edgecolor='black')
plt.title('Numero de Jogos Vs Total de Gols')
plt.xlabel('Numero de Jogos')
plt.ylabel('Total de Gols')
plt.yticks(range(data.index.max() + 1))
plt.show()
