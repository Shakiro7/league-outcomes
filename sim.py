"""
League simulator that simulates the remaining matches of a league season and calculates 
the probability of a specific team finishing in each position.
"""

import random
from collections import Counter
import click
from utils import read_csv_table, read_csv_fixtures


def simulate_game():
    """
    Simuliert ein Spiel zwischen zwei Teams und gibt die Tore zurück.
    Returns:
        tuple: Ein Tupel mit den Toren des Heim- und Auswärtsteams.
    """
    return random.randint(0, 3), random.randint(0, 3)


def simulate_game_realgoals():
    """
    Simuliert ein Spiel zwischen zwei Teams basierend auf realistischeren Ergebniswahrscheinlichkeiten.
    Returns:
        tuple: Ein Tupel mit den Toren des Heim- und Auswärtsteams.
    """

    # Gewichtete Wahrscheinlichkeiten für Tore (z.B. 0 Tore häufiger als 3+ Tore)
    torverteilung = [0, 1, 2, 3, 4]         # mögliche Tore
    torgewichte_heim =  [54/261, 87/261, 61/261, 40/261, 19/261]
    torgewichte_auswärts = [76/261, 80/261, 61/261, 25/261, 19/261]

    tore_heim = random.choices(torverteilung, weights=torgewichte_heim, k=1)[0]
    tore_auswärts = random.choices(torverteilung, weights=torgewichte_auswärts, k=1)[0]

    return tore_heim, tore_auswärts


def update_table(table_dict, home, away, home_goals, away_goals):
    """
    Aktualisiert die Tabelle mit den Ergebnissen eines Spiels.
    Args:
        table_dict (dict): Die Tabelle als Dictionary.
        home (str): Der Name des Heimteams.
        away (str): Der Name des Auswärtsteams.
        home_goals (int): Die Tore des Heimteams.
        away_goals (int): Die Tore des Auswärtsteams.
    """
    if home not in table_dict or away not in table_dict:
        return

    home_team = table_dict[home]
    away_team = table_dict[away]

    home_team["Spiele"] += 1
    away_team["Spiele"] += 1

    home_team["Tore"] += home_goals
    home_team["Gegentore"] += away_goals

    away_team["Tore"] += away_goals
    away_team["Gegentore"] += home_goals

    home_team["Differenz"] = home_team["Tore"] - home_team["Gegentore"]
    away_team["Differenz"] = away_team["Tore"] - away_team["Gegentore"]

    if home_goals > away_goals:
        home_team["Punkte"] += 3
        home_team["Siege"] += 1
        away_team["Niederlagen"] += 1
    elif home_goals < away_goals:
        away_team["Punkte"] += 3
        away_team["Siege"] += 1
        home_team["Niederlagen"] += 1
    else:
        home_team["Punkte"] += 1
        away_team["Punkte"] += 1
        home_team["Unentschieden"] += 1
        away_team["Unentschieden"] += 1


# CLI mit Click
@click.command()
@click.option(
    "--tabelle",
    prompt="Pfad zur CSV-Datei mit der Tabelle",
    help="Pfad zur aktuellen Tabelle im CSV-Format",
)
@click.option(
    "--spiele",
    prompt="Pfad zur CSV-Datei mit verbleibenden Spielen",
    help="Pfad zu den verbleibenden Spielen",
)
@click.option(
    "--team",
    prompt="Teamname",
    help="Name des Teams für die Wahrscheinlichkeitsanalyse",
)
@click.option("--anzahl", default=1000, help="Anzahl der Simulationen (Default: 1000)")
def simulate_season(tabelle, spiele, team, anzahl):
    """
    Simuliert die verbleibenden Spiele einer Saison und berechnet die 
    Platzierungswahrscheinlichkeiten für ein Team.
    Args:
        tabelle (str): Pfad zur CSV-Datei mit der Tabelle.
        spiele (str): Pfad zur CSV-Datei mit den verbleibenden Spielen.
        team (str): Name des Teams für die Wahrscheinlichkeitsanalyse.
        anzahl (int): Anzahl der Simulationen.
    """
    print(f"Simuliere Saison für {team} mit {anzahl} Simulationen...")
    table_raw = read_csv_table(tabelle)
    fixtures = read_csv_fixtures(spiele)

    platzierungsstatistik = Counter()
    ergebnis_counter = Counter()

    for sim in range(anzahl):
        # Tabelle in dict-Form umwandeln
        table = {}
        for row in table_raw:
            table[row["Team"]] = {
                "Team": row["Team"],
                "Spiele": int(row["Spiele"]),
                "Siege": int(row["Siege"]),
                "Unentschieden": int(row["Unentschieden"]),
                "Niederlagen": int(row["Niederlagen"]),
                "Tore": int(row["Tore"].split(":")[0]),
                "Gegentore": int(row["Tore"].split(":")[1]),
                "Differenz": int(row["Differenz"]),
                "Punkte": int(row["Punkte"]),
            }

        # Spiele simulieren
        # print(f"Simulation {sim + 1}/{anzahl}...")
        for heim, auswärts in fixtures:
            tore_heim, tore_auswärts = simulate_game_realgoals()
            # print(f"Simuliere Spiel: {heim} vs {auswärts} -> {tore_heim}:{tore_auswärts}")
            
            # Tabelle aktualisieren
            update_table(table, heim, auswärts, tore_heim, tore_auswärts)
            
            # Spielergebnis aus Sicht des Heimteams zählen
            if tore_heim > tore_auswärts:
                ergebnis_counter["Sieg"] += 1
            elif tore_heim < tore_auswärts:
                ergebnis_counter["Niederlage"] += 1
            else:
                ergebnis_counter["Unentschieden"] += 1

        # Tabelle sortieren nach Punkte, Differenz, Tore
        sorted_table = sorted(
            table.values(),
            key=lambda x: (x["Punkte"], x["Differenz"], x["Tore"]),
            reverse=True,
        )
        # print(f"Sortierte Tabelle nach Simulation {sim + 1}:")
        # for i, row in enumerate(sorted_table):
            # print(
            #     f"{i + 1}. {row['Team']} - Punkte: {row['Punkte']}, "
            #     f"Differenz: {row['Differenz']}, Tore: {row['Tore']}"
            # )

        for i, row in enumerate(sorted_table):
            if row["Team"].lower() == team.lower():
                platzierungsstatistik[i + 1] += 1
                break

    # Ergebnisse anzeigen
    print(f"\nPlatzierungs-Wahrscheinlichkeiten für {team}:")
    for platz in range(1, 19):
        wahrscheinlichkeit = (platzierungsstatistik[platz] / anzahl) * 100
        print(f"Platz {platz}: {wahrscheinlichkeit:.2f} %")

    # Verteilung der Spielergebnisse anzeigen
    total = sum(ergebnis_counter.values())
    print("\nVerteilung der Spielergebnisse (aus Sicht des Heimteams):")
    for ergebnis, anzahl in ergebnis_counter.items():
        prozent = anzahl / total * 100
        print(f"{ergebnis:<13}: {anzahl:>4} Spiele ({prozent:.2f}%)")

if __name__ == "__main__":
    simulate_season() # pylint: disable=no-value-for-parameter
