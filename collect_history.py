import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("JCDECAUX_API_KEY")
CONTRACT = os.getenv("JCDECAUX_CONTRACT")

# Récupération des données des stations
base_url = "https://api.jcdecaux.com/vls/v3/stations"
params = f"?contract={CONTRACT}&apiKey={API_KEY}"
url = base_url + params
response = requests.get(url)
stations = response.json()

# Transformation en DataFrame
stations_df = pd.DataFrame(stations)

# Ajout du timestamp
stations_df["snapshot_time"] = datetime.now().isoformat()

# Enregistrement dans le CSV (ajout ou création)
history_file = os.path.join(BASE_DIR, "stations_history.csv")
if not os.path.isfile(history_file):
    stations_df.to_csv(history_file, index=False)
else:
    stations_df.to_csv(history_file, mode="a", header=False, index=False)

print(f"Snapshot enregistré à {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
