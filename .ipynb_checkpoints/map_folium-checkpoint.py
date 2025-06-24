import os
import pandas as pd
import folium
from folium import CircleMarker
from ipywidgets import interact, IntSlider
from datetime import datetime

try:
    from matplotlib import cm
    import matplotlib.colors as mcolors
except ImportError:
    raise ImportError("Veuillez installer matplotlib : pip install matplotlib")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
history_file = os.path.join(BASE_DIR, "stations_history.csv")

df = pd.read_csv(history_file)
df["snapshot_time"] = pd.to_datetime(df["snapshot_time"])

# Vérifie les noms de colonnes pour latitude/longitude
lat_col = "position.latitude"
lon_col = "position.longitude"
bikes_col = "mainStands.availabilities.bikes"

if lat_col not in df.columns or lon_col not in df.columns:
    raise ValueError(f"Colonnes {lat_col} ou {lon_col} absentes du CSV.")

# Liste des timestamps uniques (pour le slider)
timestamps = sorted(df["snapshot_time"].unique())
min_bikes = df[bikes_col].min()
max_bikes = df[bikes_col].max()


def color_scale(val, vmin, vmax):
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap("RdYlGn")
    rgb = cmap(norm(val))[:3]
    return mcolors.rgb2hex(rgb)


def plot_map(snapshot_idx):
    snapshot = timestamps[snapshot_idx]
    d = df[df["snapshot_time"] == snapshot]
    m = folium.Map(location=[43.6045, 1.4440], zoom_start=13)
    for _, row in d.iterrows():
        color = color_scale(row[bikes_col], min_bikes, max_bikes)
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['name']}<br>Vélos dispo : {row[bikes_col]}",
        ).add_to(m)
    return m


if __name__ == "__main__":
    interact(
        plot_map,
        snapshot_idx=IntSlider(
            min=0,
            max=len(timestamps) - 1,
            step=1,
            value=0,
            description="Instant T",
            continuous_update=False,
        ),
    )
    print("Utilise ce script dans un notebook Jupyter pour voir la carte interactive.")
