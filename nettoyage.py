
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




