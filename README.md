# Vélo Toulouse - Statistiques et Visualisation

Ce projet permet d'explorer et de visualiser les données des vélos en libre service à Toulouse (Vélo Toulouse) grâce à l'API JCDecaux et à l'outil interactif PyGWalker.

## Fonctionnalités

- Récupération automatique des données des stations Vélo Toulouse via l'API JCDecaux
- Exploration et visualisation interactive des données (graphiques, filtres, cartes, etc.)
- Statistiques personnalisables sur la disponibilité des vélos, l'état des stations, etc.

## Prérequis

- Python 3.8 ou plus
- Un navigateur web

## Installation

1. **Clone ou télécharge ce dépôt**
2. **Installe les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Crée un fichier `.env` à la racine du projet** avec :
   ```env
   JCDECAUX_API_KEY=ta_clé_api_jcdecaux
   JCDECAUX_CONTRACT=Toulouse
   ```
   (Remplace `ta_clé_api_jcdecaux` par ta propre clé, à obtenir sur https://developer.jcdecaux.com/#/opendata/vls?page=getstarted)

## Utilisation

### 1. Lancer Jupyter Notebook

```bash
pip install notebook
jupyter notebook
```

### 2. Créer un nouveau notebook Python

- Clique sur "New" > "Python 3"
- Copie le code de `main.py` dans une cellule et exécute-la

### 3. Explorer les données

- Utilise l'interface PyGWalker qui s'affiche pour créer des graphiques, filtrer, explorer les stations, etc.

## Exemples d'analyses

- Nombre de vélos disponibles par station
- Répartition des stations ouvertes/fermées
- Carte des stations
- Stations avec le plus de vélos ou d'emplacements libres

## Ressources

- [Documentation officielle JCDecaux](https://developer.jcdecaux.com/#/opendata/vls?page=getstarted)
- [PyGWalker](https://github.com/Kanaries/pygwalker)

## Aide

Pour toute question ou suggestion, ouvre une issue ou contacte le mainteneur du projet.
