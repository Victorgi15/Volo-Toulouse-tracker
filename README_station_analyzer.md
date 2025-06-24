# 🚲 Analyseur de Stations Vélô'Toulouse

Ce programme Python permet d'analyser les stations de vélos Vélô'Toulouse et de visualiser l'évolution du nombre de vélos disponibles au fil du temps.

## 📋 Fonctionnalités

- **Affichage des stations** : Liste toutes les stations avec leur statut actuel (disponibilité, capacité)
- **Sélection interactive** : Interface en ligne de commande pour choisir une station
- **Graphiques d'évolution** : Visualisation de l'évolution du nombre de vélos sur 24h
- **Statistiques détaillées** : Moyenne, min/max, heures de pointe, etc.

## 🛠️ Installation

1. Assurez-vous d'avoir Python installé (version 3.7+)
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## 📊 Utilisation

### Lancement du programme

```bash
python station_analyzer.py
```

### Interface utilisateur

1. **Affichage des stations** : Le programme affiche automatiquement la liste des stations avec :

   - 🟢 Stations bien remplies (>70%)
   - 🟡 Stations moyennement remplies (30-70%)
   - 🔴 Stations peu remplies (<30%)

2. **Sélection d'une station** : Entrez le numéro de la station que vous souhaitez analyser

3. **Visualisation** : Le programme génère automatiquement :

   - Un graphique d'évolution du nombre de vélos
   - Un graphique de pourcentage de remplissage
   - Des statistiques détaillées

4. **Continuer** : Choisissez si vous voulez analyser une autre station

## 📁 Fichiers de données

Le programme utilise par ordre de priorité :

1. `stations_history.csv` - Données historiques complètes (si disponible)
2. `demo-source-data.csv` - Données de démonstration (si le fichier principal n'existe pas)

## 📈 Exemple de sortie

```
🚲 ANALYSEUR DE STATIONS VÉLO'TÔULOUSE
==================================================

================================================================================
🚲 STATIONS DE VÉLOS VÉLO'TÔULOUSE
================================================================================

📊 385 stations disponibles:

🟢 277 | 00277 - ZAMENHOF
    📍 10/12 RUE ZAMENHOF
    🚲 13.8/18 vélos disponibles (76.7%)

🎯 SÉLECTION D'UNE STATION
----------------------------------------
 1. 1 - 00001 - POIDS DE L'HUILE
 2. 2 - 00002 - LAFAYETTE
 ...

📈 STATISTIQUES - 00277 - ZAMENHOF
--------------------------------------------------
🚲 Nombre moyen de vélos: 13.8
📊 Nombre minimum: 0
📈 Nombre maximum: 18
📏 Écart-type: 4.7
🏗️  Capacité totale: 18
💯 Taux de remplissage moyen: 76.7%
⏰ Heure de pointe (plus de vélos): 10h
🌙 Heure creuse (moins de vélos): 18h
```

## 🔧 Dépendances

- `pandas` : Manipulation des données
- `matplotlib` : Création des graphiques
- `numpy` : Calculs numériques
- `ast` : Parsing des données JSON dans les CSV

## 📝 Notes techniques

- Le programme gère automatiquement les données manquantes
- Les graphiques s'adaptent automatiquement à la résolution d'écran
- Interface en français avec émojis pour une meilleure lisibilité
- Gestion d'erreurs robuste pour les données corrompues

## 🚀 Améliorations possibles

- Ajout de filtres par zone géographique
- Comparaison entre plusieurs stations
- Export des graphiques en PNG/PDF
- Interface web avec Flask/Dash
- Prédiction de disponibilité future
