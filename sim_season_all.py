"""
Simuliert die verbleibenden Spiele einer Saison für alle Teams und erstellt eine Heatmap
der Platzierungswahrscheinlichkeiten.
"""

import datetime
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sim import simulate_game_realgoals, update_table
from utils import read_csv_table, read_csv_fixtures


def simulate_season_for_all_teams(
    tabelle_path=None,
    spiele_path=None,
    table_raw=None,
    fixtures=None,
    runs=1000,
    export=False,
    torverteilung=None,
    torgewichte_heim=None,
    torgewichte_auswaerts=None,
):
    """
    Simuliert die verbleibenden Spiele einer Saison für alle Teams und erstellt eine Heatmap
    der Platzierungswahrscheinlichkeiten.
    Args:
        tabelle_path (str): Pfad zur CSV-Datei mit der Tabelle (optional, falls table_raw übergeben wird).
        spiele_path (str): Pfad zur CSV-Datei mit den verbleibenden Spielen (optional, falls fixtures übergeben wird).
        table_raw (list of dict): Bereits eingelesene Tabelle (optional).
        fixtures (list of tuples): Bereits eingelesene Spielpaarungen (optional).
        runs (int): Anzahl der durchzuführenden Simulationen.
        export (bool): Ob die Heatmap exportiert werden soll.
        torverteilung (list): Optionale Torverteilung für die Simulation.
        torgewichte_heim (list): Optionale Heimtor-Gewichte.
        torgewichte_auswaerts (list): Optionale Auswärtstor-Gewichte.
    """
    print(f"Simuliere {runs} Saisons...")

    # Falls Daten nicht direkt übergeben wurden, per CSV einlesen
    if table_raw is None:
        if tabelle_path is None:
            raise ValueError(
                "Entweder tabelle_path oder table_raw muss angegeben werden."
            )
        table_raw = read_csv_table(tabelle_path)

    if fixtures is None:
        if spiele_path is None:
            raise ValueError(
                "Entweder spiele_path oder fixtures muss angegeben werden."
            )
        fixtures = read_csv_fixtures(spiele_path)

    teams = [row["Team"] for row in table_raw]
    platzierungsstatistik = {team: Counter() for team in teams}
    # Anzahl der gespielten Spieltage für später speichern
    gespielte_spieltage = int(table_raw[0]["Spiele"])

    for _ in range(runs):
        # Tabelle aufbauen
        table = {
            row["Team"]: {
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
            for row in table_raw
        }

        # Spiele simulieren
        for heim, auswaerts in fixtures:
            tore_heim, tore_auswaerts = simulate_game_realgoals(
                torverteilung=torverteilung,
                torgewichte_heim=torgewichte_heim,
                torgewichte_auswaerts=torgewichte_auswaerts,
            )
            update_table(table, heim, auswaerts, tore_heim, tore_auswaerts)

        # Tabelle sortieren
        sorted_table = sorted(
            table.values(),
            key=lambda x: (x["Punkte"], x["Differenz"], x["Tore"]),
            reverse=True,
        )

        for i, row in enumerate(sorted_table):
            platzierungsstatistik[row["Team"]][i + 1] += 1

    # Wahrscheinlichkeiten berechnen
    df = pd.DataFrame(index=range(1, len(teams) + 1), columns=teams)

    for team in teams:
        for platz in range(1, len(teams) + 1):
            wahrscheinlichkeit = platzierungsstatistik[team][platz] / runs * 100
            df.at[platz, team] = round(wahrscheinlichkeit, 2)

    df = df.sort_index(ascending=True)

    # Heatmap erzeugen
    plt.figure(figsize=(max(12, len(teams)), 10))
    sns.set(font_scale=0.9)
    ax = sns.heatmap(
        df.astype(float),
        annot=True,
        fmt=".2f",
        cmap="rocket_r",
        linewidths=0.5,
        vmin=0,
        vmax=100,
        cbar_kws={"label": "Wahrscheinlichkeit (%)"},
    )
    ax.set_title(
        f"Platzierungs-Wahrscheinlichkeiten nach Spieltag {gespielte_spieltage}",
        fontsize=16,
    )
    ax.set_xlabel("Team")
    ax.set_ylabel("Platzierung")
    plt.tight_layout()

    # Optionaler Export
    if export:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(
            f"output/platzierungsprobs_nach_spieltag_{gespielte_spieltage}_runs_{runs}_{timestamp}.png",
            dpi=300,
        )
        print("Export abgeschlossen: PNG gespeichert.")

    plt.show()


# Beispiel-Aufruf (als Skript)
if __name__ == "__main__":
    simulate_season_for_all_teams(
        tabelle_path="data/zweite_liga_tabelle_2025-04-20_16-18-22.csv",
        spiele_path="data/paarungen_ab_spieltag_31_2025-04-20_16-18-23.csv",
        runs=1000,
        export=False,
    )
