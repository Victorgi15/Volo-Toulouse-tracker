import requests
import pandas as pd
import pygwalker as pyg
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("JCDECAUX_API_KEY")
CONTRACT = os.getenv("JCDECAUX_CONTRACT")

# Récupération des données des stations
url = f"https://api.jcdecaux.com/vls/v3/stations?contract={CONTRACT}&apiKey={API_KEY}"
response = requests.get(url)
stations = response.json()

# Transformation en DataFrame
stations_df = pd.DataFrame(stations)

# Affichage interactif avec PyGWalker
pyg.walk(stations_df, env="Jupyter")
