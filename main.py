from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

url = "https://fbref.com/en/comps/9/Premier-League-Stats"

try:
    driver.get(url)
    time.sleep(3)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.stats_table")))
    team_links = []
    team_names = []
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]: 
        try:
            team_cell = row.find_element(By.CSS_SELECTOR, "td[data-stat='team']")
            link = team_cell.find_element(By.TAG_NAME, "a")
            team_name = link.text
            team_url = link.get_attribute("href")
            
            team_names.append(team_name)
            team_links.append(team_url)
        except:
            continue
        
    all_players = []
    all_matches = []
    
    for i, (team_name, team_url) in enumerate(zip(team_names, team_links), 1):
        
        driver.get(team_url)
        time.sleep(2)
        
        try:
            players_table = driver.find_element(By.CSS_SELECTOR, "table#stats_standard_9")
            players_rows = players_table.find_elements(By.TAG_NAME, "tr")
            
            for row in players_rows[2:]:  
                try:
                    joueur_cell = row.find_element(By.CSS_SELECTOR, "th[data-stat='player']")
                    joueur = joueur_cell.text
                    
                    if not joueur or joueur == "":
                        continue
                    
                    nationalite = row.find_element(By.CSS_SELECTOR, "td[data-stat='nationality']").text
                    poste = row.find_element(By.CSS_SELECTOR, "td[data-stat='position']").text
                    age = row.find_element(By.CSS_SELECTOR, "td[data-stat='age']").text.split('-')[0]  
                    matchs = row.find_element(By.CSS_SELECTOR, "td[data-stat='games']").text
                    minutes = row.find_element(By.CSS_SELECTOR, "td[data-stat='minutes']").text
                    
                    player_data = {
                        'equipe': team_name,
                        'joueur': joueur,
                        'nationalite': nationalite,
                        'poste': poste,
                        'age': age,
                        'matchs_joues': matchs,
                        'minutes': minutes
                    }
                    all_players.append(player_data)
                except:
                    continue
            
        except Exception as e:
            print(f"  ✗ Erreur joueurs: {e}")
        
        try:
            matches_table = driver.find_element(By.CSS_SELECTOR, "table#matchlogs_for")
            matches_rows = matches_table.find_elements(By.TAG_NAME, "tr")
            
            for row in matches_rows[2:]:  
                try:
                    date = row.find_element(By.CSS_SELECTOR, "th[data-stat='date']").text
                    
                    if not date or date == "":
                        continue
                    
                    domicile_exterieur = row.find_element(By.CSS_SELECTOR, "td[data-stat='venue']").text
                    adversaire = row.find_element(By.CSS_SELECTOR, "td[data-stat='opponent']").text
                    resultat = row.find_element(By.CSS_SELECTOR, "td[data-stat='result']").text
                    buts_pour = row.find_element(By.CSS_SELECTOR, "td[data-stat='goals_for']").text
                    buts_contre = row.find_element(By.CSS_SELECTOR, "td[data-stat='goals_against']").text
                    
                    match_data = {
                        'equipe': team_name,
                        'date': date,
                        'domicile_exterieur': domicile_exterieur,
                        'adversaire': adversaire,
                        'resultat': resultat,
                        'buts_pour': buts_pour,
                        'buts_contre': buts_contre
                    }
                    all_matches.append(match_data)
                except:
                    continue
            
        except Exception as e:
            print(f"  ✗ Erreur matchs: {e}")
    
    df_players = pd.DataFrame(all_players)
    df_players.to_csv('premier_league_joueurs_2024_2025.csv', index=False, encoding='utf-8')
    
    df_matches = pd.DataFrame(all_matches)
    df_matches.to_csv('premier_league_matchs_2024_2025.csv', index=False, encoding='utf-8')
    

except Exception as e:
    print(f"\n❌ Erreur: {e}")

finally:
    driver.quit()    
    
    
    
    