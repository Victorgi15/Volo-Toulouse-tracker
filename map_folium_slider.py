import os
import pandas as pd
import folium
import ast
from folium.plugins import TimestampedGeoJson
from matplotlib import cm
import matplotlib.colors as mcolors

# Chemin du fichier CSV
data_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "stations_history.csv"
)

# Lecture des données
df = pd.read_csv(data_file)
df["snapshot_time"] = pd.to_datetime(df["snapshot_time"])


def extract_lat_lon(pos_str):
    try:
        pos_dict = ast.literal_eval(pos_str)
        return pos_dict.get("latitude", None), pos_dict.get("longitude", None)
    except Exception:
        return None, None


def extract_bikes(main_stands_str):
    try:
        d = ast.literal_eval(main_stands_str)
        return d.get("availabilities", {}).get("bikes", None)
    except Exception:
        return None


df["latitude"], df["longitude"] = zip(*df["position"].map(extract_lat_lon))
df["bikes"] = df["mainStands"].map(extract_bikes)
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Générer la grille temporelle régulière (toutes les 15 minutes)
min_time = df["snapshot_time"].min()
max_time = df["snapshot_time"].max()
all_times = pd.date_range(start=min_time, end=max_time, freq="15T")

# Forward fill par station
stations = df["number"].unique()
filled_rows = []
for station in stations:
    station_df = df[df["number"] == station].set_index("snapshot_time").sort_index()
    # Reindex sur la grille régulière
    station_df = station_df.reindex(all_times, method="ffill")
    # Remettre l'identifiant de la station (car perdu lors du reindex)
    station_df["number"] = station
    filled_rows.append(station_df)

filled_df = (
    pd.concat(filled_rows).reset_index().rename(columns={"index": "snapshot_time"})
)

# Nouveau gradient : seuil vert atteint à un nombre de vélos plus bas (ex: 80e percentile)
min_bikes = filled_df["bikes"].min()
# On prend le 80e percentile comme seuil "vert"
green_threshold = filled_df["bikes"].quantile(0.8)
# On fixe le max du gradient à ce seuil (ou à 10 si tu préfères)
vmax = max(green_threshold, 1)  # éviter vmax trop bas
vmin = min_bikes


def color_scale(val, vmin, vmax):
    # Clamp la valeur pour éviter tout débordement
    val = max(min(val, vmax), vmin)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap("RdYlGn")
    rgb = cmap(norm(val))[:3]
    return mcolors.rgb2hex(rgb)


# Construction du GeoJSON temporel
features = []
for _, row in filled_df.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]) or pd.isna(row["bikes"]):
        continue
    color = color_scale(row["bikes"], min_bikes, max_bikes)
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]],
        },
        "properties": {
            "time": row["snapshot_time"].strftime("%Y-%m-%dT%H:%M:%S"),
            "style": {
                "color": color,
                "fillColor": color,
                "fillOpacity": 0.7,
                "radius": 8,
            },
            "icon": "circle",
            "popup": f"{row['name']}<br>Vélos dispo : {row['bikes']}",
        },
    }
    features.append(feature)

gj = {
    "type": "FeatureCollection",
    "features": features,
}

m = folium.Map(location=[43.6045, 1.4440], zoom_start=13)

TimestampedGeoJson(
    gj,
    period="PT15M",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY-MM-DD HH:mm:ss",
    time_slider_drag_update=True,
    duration="PT15M",
).add_to(m)

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "map_slider.html"
)
m.save(output_file)
print(f"Carte interactive générée : {output_file}")
