from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
import time

# Options pour Chrome (headless si tu veux)
opt = Options()
# opt.add_argument("--headless")  # décommente si tu veux sans interface

driver = webdriver.Chrome(options=opt)
wait = WebDriverWait(driver, 10)

url = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"

all_players = []
all_matches = []

try:
    driver.get(url)
    time.sleep(3)

    # Récupérer les équipes via un sélecteur CSS stable
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table")))
    elements = search_box.find_elements(By.CSS_SELECTOR, "tbody > tr > .left > a")
    team_names = [e.text for e in elements]
    links = [a.get_attribute("href") for a in elements]

    # Boucle sur chaque équipe
    for team_name, link in zip(team_names, links):
        driver.get(link)
        time.sleep(3)

        # Récupérer les joueurs
        try:
            players_table = driver.find_element(By.ID, "stats_standard_9")
            players_rows = players_table.find_elements(By.TAG_NAME, "tr")
            for row in players_rows[1:]:
                try:
                    joueur = row.find_element(By.CSS_SELECTOR, "th[data-stat='player']").text
                    if not joueur:
                        continue
                    player_data = {
                        'equipe': team_name,
                        'joueur': joueur,
                        'nationalite': row.find_element(By.CSS_SELECTOR, "td[data-stat='nationality']").text,
                        'poste': row.find_element(By.CSS_SELECTOR, "td[data-stat='position']").text,
                        'age': row.find_element(By.CSS_SELECTOR, "td[data-stat='age']").text.split('-')[0],
                        'matchs_joues': row.find_element(By.CSS_SELECTOR, "td[data-stat='games']").text,
                        'minutes': row.find_element(By.CSS_SELECTOR, "td[data-stat='minutes']").text
                    }
                    all_players.append(player_data)
                except:
                    continue
        except:
            print(f"Erreur récupération joueurs pour {team_name}")

        # Récupérer les matchs
        try:
            matches_table = driver.find_element(By.ID, "matchlogs_for")
            matches_rows = matches_table.find_elements(By.TAG_NAME, "tr")
            for row in matches_rows[1:]:
                try:
                    if row.find_element(By.CSS_SELECTOR, '[data-stat="comp"]').text != "Premier League":
                        continue
                    match_data = {m: row.find_element(By.CSS_SELECTOR, f'[data-stat="{m}"]').text
                                  for m in ["date", "start_time", "comp", "round", "dayofweek", "venue",
                                            "result", "goals_for", "goals_against", "opponent", "xg_for",
                                            "xg_against", "possession", "attendance", "captain", "formation",
                                            "opp_formation", "referee"]}
                    match_data['team'] = team_name
                    all_matches.append(match_data)
                except:
                    continue
        except:
            print(f"Erreur récupération matchs pour {team_name}")

    # Exporter CSV
    pd.DataFrame(all_players).to_csv('premier_league_joueurs_2024_2025.csv', index=False, encoding='utf-8')
    pd.DataFrame(all_matches).to_csv('premier_league_matchs_2024_2025.csv', index=False, encoding='utf-8')

finally:
    driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from datetime import datetime
import pandas as pd
import time

df_joueurs = pd.read_csv('premier_league_joueurs_2024_2025.csv')
df_matchs = pd.read_csv('premier_league_matchs_2024_2025.csv')

# Afficher les valeurs manquantes AVANT


print(df_joueurs.isnull().sum())

df_joueurs["minutes"].fillna(0, inplace=True)
df_joueurs["age"].fillna(0, inplace=True)


df_joueurs.dropna(subset=['poste'], inplace=True)

# Afficher les valeurs manquantes APRES
df_joueurs.isna().sum()
df_joueurs[df_joueurs.isna().any(axis=1)]

df_joueurs.loc[df_joueurs["joueur"] == "Mateus Mane", "nationalite"] = "Portugaise"
df_joueurs.loc[df_joueurs["joueur"] == "Jeremy Monga", "nationalite"] = "Française"
df_joueurs.loc[df_joueurs["joueur"] == "Jake Evans", "nationalite"] = "Anglaise"
df_joueurs.loc[df_joueurs["joueur"] == "Olabade Aluko", "nationalite"] = "Anglaise"
df_joueurs.loc[df_joueurs["joueur"] == "Tom Taylor", "nationalite"] = "Anglaise"
df_joueurs.loc[df_joueurs["joueur"] == "Jayden Moore", "nationalite"] = "Anglaise"

df_joueurs.isna().sum()
df_matchs.isna().sum()
# Supprimer les doublons


duplicates_before = df_joueurs.duplicated().sum()
print(duplicates_before)
df_joueurs = df_joueurs.drop_duplicates()
len(df_matchs)
df_matchs = df_matchs[df_matchs['venue'] == 'Home'].copy()

len(df_matchs)

# harmoniser 
df_joueurs.columns = df_joueurs.columns.str.lower().str.strip().str.replace(' ', '_')
df_matchs.columns = df_matchs.columns.str.lower().str.strip().str.replace(' ', '_')
df_joueurs.head()
# Convertir les types de données

df_joueurs["age"] = df_joueurs["age"].astype(int)
df_joueurs["minutes"] = df_joueurs["minutes"].str.replace(',', '').astype(float).astype('Int64')
df_matchs['date'] = pd.to_datetime(df_matchs['date'], format='%Y-%m-%d')
numeric_cols = ['goals_for', 'goals_against', 'xg_for', 'xg_against', 'possession']
for col in numeric_cols:
    df_matchs[col] = pd.to_numeric(df_matchs[col], errors='coerce')
text_cols_matchs = ['team', 'opponent', 'captain', 'referee', 'comp', 'round', 'venue', 'result', 'dayofweek', 'formation', 'opp_formation']
for col in text_cols_matchs:
    if col in df_matchs.columns:
        df_matchs[col] = df_matchs[col].str.strip()
        
text_cols_joueurs = ['joueur', 'equipe', 'poste', 'nationalite']
for col in text_cols_joueurs:
    if col in df_joueurs.columns:
        df_joueurs[col] = df_joueurs[col].str.strip()
    

df_joueurs.head()

df_matchs.head()




