# 🗺️ Carte Interactive Temporelle Vélô'Toulouse - `map_folium_slider.py`

Ce script crée une carte interactive temporelle des stations Vélô'Toulouse, permettant de visualiser l'évolution de la disponibilité des vélos au fil du temps avec un curseur temporel.

## 🎯 Objectif

Le script `map_folium_slider.py` génère une carte interactive HTML (`map_slider.html`) qui permet de :

- Visualiser toutes les stations Vélô'Toulouse sur une carte
- Naviguer dans le temps avec un curseur temporel
- Voir l'évolution de la disponibilité des vélos par station
- Analyser les patterns d'utilisation du réseau

## 📋 Fonctionnalités

- **Carte interactive** : Basée sur Folium avec OpenStreetMap
- **Curseur temporel** : Navigation dans le temps avec pas de 15 minutes
- **Code couleur dynamique** : Rouge (peu de vélos) → Vert (beaucoup de vélos)
- **Popups informatifs** : Nom de station et nombre de vélos disponibles
- **Interpolation temporelle** : Remplissage des données manquantes
- **Contrôles de lecture** : Play/Pause, vitesse, boucle

## 🛠️ Prérequis

### 1. Dépendances Python

```bash
pip install -r requirements.txt
```

**Dépendances spécifiques :**

- `folium` : Création de cartes interactives
- `pandas` : Manipulation des données
- `matplotlib` : Gestion des couleurs et gradients

### 2. Données requises

Le script nécessite le fichier `stations_history.csv` généré par `collect_history.py` ou des données de démonstration.

## 🚀 Utilisation

### Exécution simple

```bash
python map_folium_slider.py
```

### Résultat

Le script génère automatiquement :

- **`map_slider.html`** : Carte interactive dans votre navigateur
- **Message de confirmation** : Chemin du fichier généré

## 📊 Fonctionnement détaillé

### 1. Lecture et traitement des données

```python
# Lecture du CSV historique
df = pd.read_csv("stations_history.csv")
df["snapshot_time"] = pd.to_datetime(df["snapshot_time"])

# Extraction des coordonnées GPS
df["latitude"], df["longitude"] = zip(*df["position"].map(extract_lat_lon))

# Extraction du nombre de vélos
df["bikes"] = df["mainStands"].map(extract_bikes)
```

### 2. Interpolation temporelle

Le script crée une grille temporelle régulière (toutes les 15 minutes) et remplit les données manquantes :

```python
# Grille temporelle régulière
all_times = pd.date_range(start=min_time, end=max_time, freq="15T")

# Forward fill par station
for station in stations:
    station_df = df[df["number"] == station].set_index("snapshot_time").sort_index()
    station_df = station_df.reindex(all_times, method="ffill")
```

### 3. Code couleur dynamique

Le gradient de couleurs s'adapte automatiquement aux données :

- **🔴 Rouge** : Stations avec peu de vélos disponibles
- **🟡 Jaune** : Stations moyennement remplies
- **🟢 Vert** : Stations bien remplies (80e percentile)

```python
# Seuil vert basé sur le 80e percentile
green_threshold = filled_df["bikes"].quantile(0.8)
vmax = max(green_threshold, 1)
```

### 4. Génération de la carte

```python
# Carte centrée sur Toulouse
m = folium.Map(location=[43.6045, 1.4440], zoom_start=13)

# Ajout du curseur temporel
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
```

## 🎮 Contrôles de la carte interactive

Une fois la carte ouverte dans votre navigateur :

### Curseur temporel

- **Glisser** : Naviguer dans le temps
- **Clic** : Aller à un moment précis
- **Boutons +/-** : Avancer/reculer d'un pas

### Contrôles de lecture

- **▶️ Play** : Lecture automatique
- **⏸️ Pause** : Arrêter la lecture
- **🔄 Loop** : Lecture en boucle
- **⚡ Vitesse** : Ajuster la vitesse de lecture

### Navigation

- **Zoom** : Molette de souris ou boutons +/-
- **Déplacement** : Clic et glisser
- **Popups** : Clic sur une station pour les détails

## 📁 Fichiers générés

### `map_slider.html`

Fichier HTML autonome contenant :

- Carte interactive Folium
- Curseur temporel intégré
- Données JSON temporelles
- Styles CSS personnalisés

**Taille typique** : 3-5 MB (selon la quantité de données)

## 🔧 Personnalisation

### Modifier la fréquence temporelle

```python
# Changer de 15 minutes à 30 minutes
all_times = pd.date_range(start=min_time, end=max_time, freq="30T")
```

### Ajuster le code couleur

```python
# Changer le seuil vert (actuellement 80e percentile)
green_threshold = filled_df["bikes"].quantile(0.9)  # 90e percentile

# Utiliser une palette différente
cmap = cm.get_cmap("viridis")  # Au lieu de "RdYlGn"
```

### Modifier la taille des points

```python
# Dans la génération des features
"radius": 12,  # Au lieu de 8
```

### Changer le centre de la carte

```python
# Coordonnées de Toulouse (latitude, longitude)
m = folium.Map(location=[43.6045, 1.4440], zoom_start=12)
```

## 📈 Exemples d'analyses possibles

### Patterns temporels

- **Heures de pointe** : Identifier les moments de forte utilisation
- **Stations critiques** : Repérer les stations souvent vides ou pleines
- **Évolution quotidienne** : Voir les cycles d'utilisation

### Analyses spatiales

- **Zones de concentration** : Identifier les zones avec beaucoup de stations
- **Déserts de vélos** : Repérer les zones mal desservies
- **Corridors d'utilisation** : Analyser les flux de vélos

## ⚠️ Limitations et bonnes pratiques

### Limitations techniques

- **Taille du fichier** : Peut devenir volumineux avec beaucoup de données
- **Performance navigateur** : Limitation avec de très grandes quantités de données
- **Données manquantes** : L'interpolation peut masquer des problèmes de données

### Recommandations

- **Fréquence de collecte** : Collectez des données toutes les 15-30 minutes
- **Période d'analyse** : Limitez à quelques jours pour de meilleures performances
- **Sauvegarde** : Sauvegardez régulièrement le fichier HTML généré

## 🐛 Dépannage

### Erreur "File not found"

- Vérifiez que `stations_history.csv` existe
- Lancez d'abord `collect_history.py` pour générer des données

### Carte vide

- Vérifiez que les données contiennent des coordonnées GPS valides
- Assurez-vous que les données temporelles sont correctes

### Performance lente

- Réduisez la période d'analyse
- Augmentez l'intervalle temporel (30 minutes au lieu de 15)
- Vérifiez la taille du fichier CSV

### Problèmes d'affichage

- Ouvrez le fichier HTML dans un navigateur moderne
- Vérifiez que JavaScript est activé
- Essayez un autre navigateur

## 🔗 Intégration avec d'autres outils

### Avec `collect_history.py`

```bash
# 1. Collecter des données
python collect_history.py

# 2. Générer la carte
python map_folium_slider.py
```

### Avec `station_analyzer.py`

- Utilisez la carte pour identifier les stations intéressantes
- Analysez ensuite ces stations en détail avec l'analyseur

## 📞 Support

Pour toute question ou problème :

1. Vérifiez que toutes les dépendances sont installées
2. Assurez-vous que le fichier CSV contient des données valides
3. Consultez la [documentation Folium](https://python-visualization.github.io/folium/)
4. Ouvrez une issue sur le projet

## 🔗 Liens utiles

- [Documentation Folium](https://python-visualization.github.io/folium/)
- [Plugin TimestampedGeoJson](https://python-visualization.github.io/folium/plugins.html#timestampedgeojson)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [Analyseur de stations](./README_station_analyzer.md)
- [Collecte de données](./README_collect_history.md)
