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
