import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import ast
import os


class StationAnalyzer:
    def __init__(self, data_file="demo-source-data.csv"):
        """Initialise l'analyseur de stations avec les données"""
        self.data_file = data_file
        self.stations_data = None
        self.load_data()

    def load_data(self):
        """Charge et traite les données des stations"""
        try:
            # Charger les données CSV
            self.stations_data = pd.read_csv(self.data_file)

            # Nettoyer et traiter les données
            self.process_data()

        except FileNotFoundError:
            print(f"Erreur: Le fichier {self.data_file} n'a pas été trouvé.")
            print("Utilisation de données de démonstration...")
            self.create_demo_data()

    def process_data(self):
        """Traite les données pour extraire les informations utiles"""
        if self.stations_data is None:
            return

        # Extraire le nombre de vélos depuis la colonne totalStands
        def extract_bikes(row):
            try:
                if pd.notna(row["totalStands"]):
                    data = ast.literal_eval(row["totalStands"])
                    return data["availabilities"]["bikes"]
                return 0
            except (ValueError, SyntaxError, KeyError):
                return 0

        def extract_capacity(row):
            try:
                if pd.notna(row["totalStands"]):
                    data = ast.literal_eval(row["totalStands"])
                    return data["capacity"]
                return 0
            except (ValueError, SyntaxError, KeyError):
                return 0

        # Ajouter les colonnes calculées
        self.stations_data["bikes_available"] = self.stations_data.apply(
            extract_bikes, axis=1
        )
        self.stations_data["capacity"] = self.stations_data.apply(
            extract_capacity, axis=1
        )

        # Convertir snapshot_time en datetime
        self.stations_data["snapshot_time"] = pd.to_datetime(
            self.stations_data["snapshot_time"]
        )

    def create_demo_data(self):
        """Crée des données de démonstration avec évolution temporelle"""
        # Stations de base
        base_stations = [
            {
                "number": 385,
                "name": "00385 - VITARELLES - FRONDE",
                "address": "21, chemin de la Fronde",
            },
            {
                "number": 195,
                "name": "00195 - RIEUX - CHANT DU MERLE",
                "address": "FACE 15 RUE PIERRE LAROUSSE",
            },
            {"number": 29, "name": "00029 - VALADE", "address": "31 RUE VALADE"},
            {
                "number": 400,
                "name": "00400 - SAINT-MARTIN-DU-TOUCH GARE",
                "address": "4, rue Marie Louise Dissard",
            },
            {
                "number": 156,
                "name": "00156 - EMPALOT - MÉTRO",
                "address": "38 AV JEAN MOULIN",
            },
        ]

        # Générer des données temporelles (24 heures avec des mesures toutes les heures)
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_points = [start_time + timedelta(hours=i) for i in range(24)]

        # Créer des données pour chaque station
        demo_data = []
        for station in base_stations:
            # Générer un pattern réaliste pour chaque station
            base_bikes = np.random.randint(5, 15)
            capacity = base_bikes + np.random.randint(5, 10)

            for i, time_point in enumerate(time_points):
                # Pattern quotidien: plus de vélos le matin et le soir
                hour = time_point.hour
                if 7 <= hour <= 9:  # Heures de pointe matin
                    bikes = max(0, min(capacity, base_bikes + np.random.randint(-2, 8)))
                elif 17 <= hour <= 19:  # Heures de pointe soir
                    bikes = max(0, min(capacity, base_bikes + np.random.randint(-2, 8)))
                else:  # Heures creuses
                    bikes = max(0, min(capacity, base_bikes + np.random.randint(-5, 5)))

                demo_data.append(
                    {
                        "number": station["number"],
                        "name": station["name"],
                        "address": station["address"],
                        "bikes_available": bikes,
                        "capacity": capacity,
                        "snapshot_time": time_point,
                    }
                )

        self.stations_data = pd.DataFrame(demo_data)

    def display_stations(self):
        """Affiche la liste des stations disponibles"""
        print("\n" + "=" * 80)
        print("🚲 STATIONS DE VÉLOS VÉLO'TÔULOUSE")
        print("=" * 80)

        if self.stations_data is None or self.stations_data.empty:
            print("Aucune donnée de station disponible.")
            return

        # Grouper par station pour afficher les informations uniques
        unique_stations = (
            self.stations_data.groupby(["number", "name", "address"])
            .agg({"bikes_available": "mean", "capacity": "first"})
            .round(1)
            .reset_index()
        )

        print(f"\n📊 {len(unique_stations)} stations disponibles:\n")

        for idx, station in unique_stations.iterrows():
            station_num = station["number"]
            name = station["name"]
            address = station["address"]
            avg_bikes = station["bikes_available"]
            capacity = station["capacity"]

            # Calculer le pourcentage de remplissage
            fill_percentage = (avg_bikes / capacity * 100) if capacity > 0 else 0

            # Indicateur visuel de disponibilité
            if fill_percentage > 70:
                status = "🟢"
            elif fill_percentage > 30:
                status = "🟡"
            else:
                status = "🔴"

            print(f"{status} {station_num:3d} | {name}")
            print(f"    📍 {address}")
            print(
                f"    🚲 {avg_bikes:.1f}/{capacity} vélos disponibles ({fill_percentage:.1f}%)"
            )
            print()

    def select_station(self):
        """Permet à l'utilisateur de sélectionner une station"""
        if self.stations_data is None or self.stations_data.empty:
            print("Aucune donnée disponible pour la sélection.")
            return None

        # Obtenir la liste des stations uniques
        unique_stations = (
            self.stations_data.groupby(["number", "name"]).first().reset_index()
        )

        print("\n🎯 SÉLECTION D'UNE STATION")
        print("-" * 40)

        for idx, station in unique_stations.iterrows():
            print(f"{idx + 1:2d}. {station['number']} - {station['name']}")

        while True:
            try:
                msg = f"\nChoisissez une station (1-{len(unique_stations)}) ou 'q' pour quitter: "
                choice = input(msg)

                if choice.lower() == "q":
                    return None

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(unique_stations):
                    selected_station = unique_stations.iloc[choice_idx]
                    return selected_station
                else:
                    print(
                        f"❌ Veuillez entrer un nombre entre 1 et {len(unique_stations)}"
                    )

            except ValueError:
                print("❌ Veuillez entrer un nombre valide")

    def plot_station_evolution(self, station):
        """Affiche un graphique de l'évolution du nombre de vélos pour une station"""
        if station is None:
            return

        station_number = station["number"]
        station_name = station["name"]

        # Filtrer les données pour cette station
        station_data = self.stations_data[
            self.stations_data["number"] == station_number
        ].copy()

        if station_data.empty:
            print(f"❌ Aucune donnée trouvée pour la station {station_number}")
            return

        # Trier par temps
        station_data = station_data.sort_values("snapshot_time")

        # Créer le graphique
        plt.figure(figsize=(12, 8))

        # Graphique principal
        plt.subplot(2, 1, 1)
        plt.plot(
            station_data["snapshot_time"],
            station_data["bikes_available"],
            marker="o",
            linewidth=2,
            markersize=6,
            color="#2E86AB",
        )
        plt.fill_between(
            station_data["snapshot_time"],
            station_data["bikes_available"],
            alpha=0.3,
            color="#2E86AB",
        )

        # Ligne de capacité
        capacity = station_data["capacity"].iloc[0]
        plt.axhline(
            y=capacity,
            color="red",
            linestyle="--",
            alpha=0.7,
            label=f"Capacité totale ({capacity} vélos)",
        )

        plt.title(
            f"🚲 Évolution du nombre de vélos disponibles\n{station_name}",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )
        plt.ylabel("Nombre de vélos disponibles", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Formatage de l'axe des temps
        plt.gcf().autofmt_xdate()

        # Graphique de pourcentage de remplissage
        plt.subplot(2, 1, 2)
        fill_percentage = station_data["bikes_available"] / capacity * 100
        plt.plot(
            station_data["snapshot_time"],
            fill_percentage,
            marker="s",
            linewidth=2,
            markersize=6,
            color="#A23B72",
        )
        plt.fill_between(
            station_data["snapshot_time"], fill_percentage, alpha=0.3, color="#A23B72"
        )

        # Lignes de référence
        plt.axhline(
            y=80, color="red", linestyle="--", alpha=0.5, label="80% (Station pleine)"
        )
        plt.axhline(
            y=20, color="orange", linestyle="--", alpha=0.5, label="20% (Station vide)"
        )

        plt.title(
            "📊 Pourcentage de remplissage de la station",
            fontsize=12,
            fontweight="bold",
        )
        plt.ylabel("Pourcentage de remplissage (%)", fontsize=12)
        plt.xlabel("Heure de la journée", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Formatage de l'axe des temps
        plt.gcf().autofmt_xdate()

        plt.tight_layout()
        plt.show()

        # Afficher des statistiques
        self.display_station_stats(station_data, station_name)

    def display_station_stats(self, station_data, station_name):
        """Affiche les statistiques de la station"""
        print(f"\n📈 STATISTIQUES - {station_name}")
        print("-" * 50)

        bikes_data = station_data["bikes_available"]
        capacity = station_data["capacity"].iloc[0]

        print(f"🚲 Nombre moyen de vélos: {bikes_data.mean():.1f}")
        print(f"📊 Nombre minimum: {bikes_data.min()}")
        print(f"📈 Nombre maximum: {bikes_data.max()}")
        print(f"📏 Écart-type: {bikes_data.std():.1f}")
        print(f"🏗️  Capacité totale: {capacity}")
        print(
            f"💯 Taux de remplissage moyen: {(bikes_data.mean() / capacity * 100):.1f}%"
        )

        # Heures de pointe
        station_data_with_hour = station_data.copy()
        station_data_with_hour["hour"] = station_data_with_hour["snapshot_time"].dt.hour

        peak_hour = station_data_with_hour.loc[
            station_data_with_hour["bikes_available"].idxmax(), "hour"
        ]
        low_hour = station_data_with_hour.loc[
            station_data_with_hour["bikes_available"].idxmin(), "hour"
        ]

        print(f"⏰ Heure de pointe (plus de vélos): {peak_hour:02d}h")
        print(f"🌙 Heure creuse (moins de vélos): {low_hour:02d}h")

    def run(self):
        """Lance l'application interactive"""
        print("🚲 ANALYSEUR DE STATIONS VÉLO'TÔULOUSE")
        print("=" * 50)

        while True:
            # Afficher les stations
            self.display_stations()

            # Sélectionner une station
            selected_station = self.select_station()

            if selected_station is None:
                print("\n👋 Au revoir!")
                break

            # Afficher le graphique
            self.plot_station_evolution(selected_station)

            # Demander si l'utilisateur veut continuer
            continue_choice = input("\nVoulez-vous analyser une autre station? (o/n): ")
            if continue_choice.lower() not in ["o", "oui", "y", "yes"]:
                print("\n👋 Au revoir!")
                break


def main():
    """Fonction principale"""
    # Essayer d'abord avec stations_history.csv, sinon utiliser demo-source-data.csv
    data_file = "stations_history.csv"
    if not os.path.exists(data_file):
        data_file = "demo-source-data.csv"
        print("⚠️  Utilisation des données de démonstration")
        print("(stations_history.csv non trouvé)")

    analyzer = StationAnalyzer(data_file)
    analyzer.run()


if __name__ == "__main__":
    main()
