import pandas as pd
import random

# -----------------------------
# Generate mock competitors
# -----------------------------
countries = ['USA', 'Croatia', 'Spain', 'Serbia', 'Germany', 'France', 'Australia', 'UK']
competitors = []

for i in range(1, 51):  # 50 competitors
    competitor_id = f"sr:competitor:{100+i}"
    name = f"Player {i}"
    country = random.choice(countries)
    abbreviation = name.split()[1][:3].upper()
    competitors.append([competitor_id, name, country, country[:3].upper(), abbreviation])

df_competitors = pd.DataFrame(competitors, columns=['competitor_id','name','country','country_code','abbreviation'])
df_competitors.to_csv('C:/Users/susen/Desktop/Tennis Game/data/processed/competitors_mock.csv', index=False)

# -----------------------------
# Generate mock rankings
# -----------------------------
rankings = []
for i, row in df_competitors.iterrows():
    rank = i+1
    points = random.randint(500, 9200)
    movement = random.choice([-2,-1,0,1,2])
    competitions_played = random.randint(10, 20)
    rankings.append([rank, movement, points, competitions_played, row['competitor_id']])

df_rankings = pd.DataFrame(rankings, columns=['rank','movement','points','competitions_played','competitor_id'])
df_rankings.to_csv('C:/Users/susen/Desktop/Tennis Game/data/processed/competitor_rankings_mock.csv', index=False)

print("✅ Mock competitors and rankings generated successfully!")
