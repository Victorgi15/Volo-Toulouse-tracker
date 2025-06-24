# 📊 Collecte de Données Vélô'Toulouse - `collect_history.py`

Ce script permet de collecter automatiquement les données des stations Vélô'Toulouse via l'API JCDecaux et de les sauvegarder dans un fichier CSV pour analyse historique.

## 🎯 Objectif

Le script `collect_history.py` effectue un "snapshot" (capture instantanée) de l'état de toutes les stations Vélô'Toulouse et l'enregistre dans `stations_history.csv`. En exécutant ce script régulièrement, vous pouvez construire une base de données historique pour analyser l'évolution de l'utilisation du réseau.

## 📋 Fonctionnalités

- **Récupération en temps réel** : Interroge l'API JCDecaux pour obtenir l'état actuel de toutes les stations
- **Sauvegarde automatique** : Ajoute chaque snapshot au fichier `stations_history.csv`
- **Gestion des erreurs** : Gestion robuste des problèmes de connexion et d'API
- **Horodatage** : Chaque enregistrement est marqué avec un timestamp précis
- **Format CSV** : Données structurées pour analyse facile

## 🛠️ Prérequis

### 1. Clé API JCDecaux

Vous devez obtenir une clé API gratuite sur le site de JCDecaux :

1. Allez sur [https://developer.jcdecaux.com/#/opendata/vls?page=getstarted](https://developer.jcdecaux.com/#/opendata/vls?page=getstarted)
2. Créez un compte gratuit
3. Demandez une clé API pour l'API VLS (Vélo en Libre Service)
4. Notez votre clé API

### 2. Dépendances Python

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Créer le fichier `.env`

Créez un fichier `.env` à la racine du projet :

```env
JCDECAUX_API_KEY=votre_clé_api_ici
JCDECAUX_CONTRACT=toulouse
```

**Exemple :**

```env
JCDECAUX_API_KEY=abc123def456ghi789
JCDECAUX_CONTRACT=toulouse
```

### 2. Vérifier la configuration

Le script utilise automatiquement :

- **Contract** : `toulouse` (pour Vélô'Toulouse)
- **API Endpoint** : `https://api.jcdecaux.com/vls/v3/stations`

## 🚀 Utilisation

### Exécution manuelle

```bash
python collect_history.py
```

### Exécution automatique (cron/task scheduler)

Pour collecter des données régulièrement, vous pouvez configurer une tâche planifiée :

#### Sur Windows (Task Scheduler)

1. Ouvrez le Planificateur de tâches
2. Créez une tâche de base
3. Définissez le déclencheur (ex: toutes les 15 minutes)
4. Action : `python C:\chemin\vers\collect_history.py`

#### Sur Linux/Mac (cron)

```bash
# Éditer le crontab
crontab -e

# Ajouter une ligne pour exécuter toutes les 15 minutes
*/15 * * * * cd /chemin/vers/velo-toulouse && python collect_history.py
```

## 📁 Fichiers générés

### `stations_history.csv`

Le script crée ou met à jour le fichier `stations_history.csv` avec les colonnes suivantes :

| Colonne          | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `number`         | Numéro unique de la station                           |
| `contractName`   | Nom du contrat (toulouse)                             |
| `name`           | Nom de la station                                     |
| `address`        | Adresse de la station                                 |
| `position`       | Coordonnées GPS (latitude/longitude)                  |
| `banking`        | Si la station accepte les paiements bancaires         |
| `bonus`          | Si c'est une station bonus                            |
| `status`         | Statut de la station (OPEN/CLOSED)                    |
| `lastUpdate`     | Dernière mise à jour de la station                    |
| `connected`      | Si la station est connectée                           |
| `overflow`       | Si la station est en débordement                      |
| `shape`          | Forme de la station                                   |
| `totalStands`    | Informations détaillées sur les vélos et emplacements |
| `mainStands`     | Emplacements principaux                               |
| `overflowStands` | Emplacements de débordement                           |
| `snapshot_time`  | Timestamp de la capture                               |

## 📊 Exemple de sortie

```
Snapshot enregistré à 2025-01-24 14:30:15
```

## 🔧 Personnalisation

### Modifier la fréquence de collecte

Pour changer la fréquence de collecte, modifiez la configuration de votre tâche planifiée :

- **Toutes les 5 minutes** : `*/5 * * * *`
- **Toutes les 30 minutes** : `*/30 * * * *`
- **Toutes les heures** : `0 * * * *`

### Changer le fichier de sortie

Modifiez la ligne dans `collect_history.py` :

```python
history_file = os.path.join(BASE_DIR, "votre_fichier.csv")
```

## 📈 Analyse des données collectées

Une fois que vous avez collecté suffisamment de données, vous pouvez les analyser avec :

1. **`station_analyzer.py`** - Interface interactive pour analyser l'évolution des stations
2. **PyGWalker** - Exploration interactive des données
3. **Pandas** - Analyse programmatique personnalisée

## ⚠️ Limitations et bonnes pratiques

### Limites de l'API JCDecaux

- **Rate limiting** : Respectez les limites de l'API (généralement 1000 requêtes/jour)
- **Clé gratuite** : Les clés gratuites ont des limitations
- **Données en temps réel** : Les données sont mises à jour toutes les 2-3 minutes

### Recommandations

- **Fréquence raisonnable** : Ne collectez pas plus d'une fois toutes les 5 minutes
- **Sauvegarde** : Sauvegardez régulièrement votre fichier `stations_history.csv`
- **Monitoring** : Surveillez la taille du fichier CSV (peut devenir volumineux)

## 🐛 Dépannage

### Erreur "API key not found"

- Vérifiez que votre fichier `.env` existe et contient la bonne clé API
- Vérifiez que la clé API est valide sur le site JCDecaux

### Erreur de connexion

- Vérifiez votre connexion internet
- L'API JCDecaux peut être temporairement indisponible

### Fichier CSV corrompu

- Sauvegardez le fichier existant
- Supprimez le fichier corrompu
- Relancez le script pour créer un nouveau fichier

## 📞 Support

Pour toute question ou problème :

1. Vérifiez que votre clé API est valide
2. Consultez la [documentation JCDecaux](https://developer.jcdecaux.com/#/opendata/vls?page=getstarted)
3. Ouvrez une issue sur le projet

## 🔗 Liens utiles

- [API JCDecaux VLS](https://developer.jcdecaux.com/#/opendata/vls?page=getstarted)
- [Documentation Vélô'Toulouse](https://velo.toulouse.fr/)
- [Analyseur de stations](./README_station_analyzer.md)
