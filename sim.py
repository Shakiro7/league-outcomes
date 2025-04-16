import click
import csv
import os
import random
import ast
from collections import defaultdict, Counter
from copy import deepcopy

# Hilfsfunktion: CSV einlesen
def read_csv_table(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_csv_fixtures(filepath):
    fixtures = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairings_str = row.get("Paarungen")
            if pairings_str:
                try:
                    pairings = ast.literal_eval(pairings_str)
                    for match in pairings:
                        if isinstance(match, list) and len(match) == 2:
                            fixtures.append((match[0].strip(), match[1].strip()))
                except (ValueError, SyntaxError):
                    print(f"⚠️ Fehler beim Parsen von Paarungen: {pairings_str}")
    return fixtures

# Hilfsfunktion: Simulation eines Spiels
def simulate_game():
    return random.randint(0, 3), random.randint(0, 3)

# Hilfsfunktion: Tabelle updaten
def update_table(table_dict, home, away, home_goals, away_goals):
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
@click.option('--tabelle', prompt='Pfad zur CSV-Datei mit der Tabelle', help='Pfad zur aktuellen Tabelle im CSV-Format')
@click.option('--spiele', prompt='Pfad zur CSV-Datei mit verbleibenden Spielen', help='Pfad zu den verbleibenden Spielen')
@click.option('--team', prompt='Teamname', help='Name des Teams für die Wahrscheinlichkeitsanalyse')
@click.option('--anzahl', default=1000, help='Anzahl der Simulationen (Standard: 1000)')
def simulate_season(tabelle, spiele, team, anzahl):
    print(f"Simuliere Saison für {team} mit {anzahl} Simulationen...")
    table_raw = read_csv_table(tabelle)
    fixtures = read_csv_fixtures(spiele)

    platzierungsstatistik = Counter()

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
                "Punkte": int(row["Punkte"])
            }
        # print(f"Initiale Tabelle:")
        # for i, row in enumerate(table.values()):
        #     print(f"{i + 1}. {row['Team']} - Punkte: {row['Punkte']}, Differenz: {row['Differenz']}, Tore: {row['Tore']}")  

        # Spiele simulieren
        print(f"Simulation {sim + 1}/{anzahl}...")
        for heim, auswärts in fixtures:
            tore_heim, tore_auswärts = simulate_game()
            print(f"Simuliere Spiel: {heim} vs {auswärts} -> {tore_heim}:{tore_auswärts}")
            # Tabelle aktualisieren
            update_table(table, heim, auswärts, tore_heim, tore_auswärts)
            # print(f"Aktualisierte Tabelle:")
            # for i, row in enumerate(table.values()):
            #     print(f"{i + 1}. {row['Team']} - Punkte: {row['Punkte']}, Differenz: {row['Differenz']}, Tore: {row['Tore']}")

        # Tabelle sortieren nach Punkte, Differenz, Tore
        sorted_table = sorted(
            table.values(),
            key=lambda x: (x["Punkte"], x["Differenz"], x["Tore"]),
            reverse=True
        )
        print(f"Sortierte Tabelle nach Simulation {sim + 1}:")
        for i, row in enumerate(sorted_table):
            print(f"{i + 1}. {row['Team']} - Punkte: {row['Punkte']}, Differenz: {row['Differenz']}, Tore: {row['Tore']}")

        for i, row in enumerate(sorted_table):
            if row["Team"].lower() == team.lower():
                platzierungsstatistik[i + 1] += 1
                break

    # Ergebnisse anzeigen
    print(f"\nPlatzierungs-Wahrscheinlichkeiten für {team}:")
    for platz in range(1, 19):
        wahrscheinlichkeit = (platzierungsstatistik[platz] / anzahl) * 100
        print(f"Platz {platz}: {wahrscheinlichkeit:.2f} %")

if __name__ == '__main__':
    simulate_season()