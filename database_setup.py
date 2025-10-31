from sqlalchemy import create_engine
from nettoyage import *

user = "postgres"
password = "abir"
host = "localhost"
port = "5432"
db = "football"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")


df_joueurs.to_sql("joueur", engine, if_exists="replace", index=False)
df_matchs.to_sql("match", engine, if_exists="replace", index=False)


