import requests
import json

# Step 1: Get the NBA Data
api_key = 'your_api_key'
url = 'https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/2023-JAN-01'
headers = {'Ocp-Apim-Subscription-Key': api_key}
response = requests.get(url, headers=headers)
data = response.json()

# Step 2: Data Storage
import psycopg2

conn = psycopg2.connect(database="nba", user="username", password="password", host="localhost", port="5432")
cursor = conn.cursor()

for game in data:
    cursor.execute("INSERT INTO games VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
        game['GameId'],
        game['AwayTeam'],
        game['HomeTeam'],
        game['AwayTeamScore'],
        game['HomeTeamScore'],
        game['DateTime'],
        game['Status'],
        game['Season'],
    ))

conn.commit()
conn.close()

# Step 3: Data Processing
import pandas as pd

df = pd.DataFrame(data)
df = df[['GameId', 'AwayTeam', 'HomeTeam', 'AwayTeamScore', 'HomeTeamScore']]
df['Winner'] = df.apply(lambda row: row['AwayTeam'] if row['AwayTeamScore'] > row['HomeTeamScore'] else row['HomeTeam'], axis=1)

# Step 4: Data Visualization
import matplotlib.pyplot as plt

plt.bar(df['Winner'].value_counts().index, df['Winner'].value_counts().values)
plt.xlabel('Team')
plt.ylabel('Wins')
plt.title('NBA Wins by Team')
plt.show()

# Step 5: Data Analysis
import numpy as np

mean = np.mean(df['HomeTeamScore'])
std = np.std(df['HomeTeamScore'])
print(f"Mean Home Team Score: {mean:.2f}")
print(f"Standard Deviation: {std:.2f}")
