import pandas as pd
import matplotlib.pyplot as plt

# Importing data from the Excel table
df = pd.read_excel('jogos.xlsx')

# Splitting the 'Placar' column into two separate columns
df[['Gols Time 1', 'Gols Time 2']] = df['Placar'].str.split(' - ', expand=True).astype(int)

# Function to plot the evolution of the number of goals scored by a team over time
def plotar_gols_time(time):
    # Filtering games in which the team participated
    time_df = df[(df['Time 1'] == time) | (df['Time 2'] == time)].copy()
    
    # Calculating the number of goals scored by the team in each game
    time_df['Gols'] = time_df.apply(lambda row: row['Gols Time 1'] if row['Time 1'] == time else row['Gols Time 2'], axis=1)
    
    # Converting the 'Data' column to datetime type
    time_df['Data'] = pd.to_datetime(time_df['Data'], format='%d/%m/%y')
    
    # Sorting the DataFrame by game date
    time_df = time_df.sort_values('Data')
    
    # Plotting the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(time_df['Data'], time_df['Gols'], marker='o')
    plt.title(f'Evolução de gols do {time}')
    plt.xlabel('Data')
    plt.ylabel('Gow ls')
    plt.xticks(rotation=45)
    plt.show()

# Example of using the function to plot the performance graph for each team separately
for time in pd.concat([df['Time 1'], df['Time 2']]).unique():
    plotar_gols_time(time)
