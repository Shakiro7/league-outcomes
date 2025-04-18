"""
League simulation CLI that simulates the remaining matches of a league season and calculates
the probability of a specific team finishing in each position.
"""

from collections import Counter
import click
from sim import simulate_game_realgoals, update_table
from utils import read_csv_table, read_csv_fixtures


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

    for _ in range(anzahl):
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
        for heim, auswaerts in fixtures:
            tore_heim, tore_auswaerts = simulate_game_realgoals()

            # Tabelle aktualisieren
            update_table(table, heim, auswaerts, tore_heim, tore_auswaerts)

            # Spielergebnis aus Sicht des Heimteams zählen
            if tore_heim > tore_auswaerts:
                ergebnis_counter["Sieg"] += 1
            elif tore_heim < tore_auswaerts:
                ergebnis_counter["Niederlage"] += 1
            else:
                ergebnis_counter["Unentschieden"] += 1

        # Tabelle sortieren nach Punkte, Differenz, Tore
        sorted_table = sorted(
            table.values(),
            key=lambda x: (x["Punkte"], x["Differenz"], x["Tore"]),
            reverse=True,
        )

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
    for ergebnis, count in ergebnis_counter.items():
        prozent = count / total * 100
        print(f"{ergebnis:<13}: {count:>4} Spiele ({prozent:.2f}%)")


if __name__ == "__main__":
    simulate_season()  # pylint: disable=no-value-for-parameter
