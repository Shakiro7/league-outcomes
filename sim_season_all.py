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


def simulate_season_for_all_teams(tabelle_path, spiele_path, anzahl=1000, export=False):
    """
    Simuliert die verbleibenden Spiele einer Saison für alle Teams und erstellt eine Heatmap
    der Platzierungswahrscheinlichkeiten.
    Args:
        tabelle_path (str): Pfad zur CSV-Datei mit der Tabelle.
        spiele_path (str): Pfad zur CSV-Datei mit den verbleibenden Spielen.
        anzahl (int): Anzahl der durchzuführenden Simulationen.
        export (bool): Ob die Heatmap exportiert werden soll.
    """
    print(f"Simuliere {anzahl} Saisons...")

    table_raw = read_csv_table(tabelle_path)
    fixtures = read_csv_fixtures(spiele_path)

    teams = [row["Team"] for row in table_raw]
    platzierungsstatistik = {team: Counter() for team in teams}

    for _ in range(anzahl):
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
            tore_heim, tore_auswaerts = simulate_game_realgoals()
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
            wahrscheinlichkeit = platzierungsstatistik[team][platz] / anzahl * 100
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
    ax.set_title("Platzierungs-Wahrscheinlichkeiten (alle Teams)", fontsize=16)
    ax.set_xlabel("Team")
    ax.set_ylabel("Platzierung")
    plt.tight_layout()

    # Optionaler Export
    if export:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f"output/platzierungsprobs_{timestamp}.png", dpi=300)
        print("Export abgeschlossen: PNG gespeichert.")

    plt.show()


# Beispiel-Aufruf (als Skript)
if __name__ == "__main__":
    simulate_season_for_all_teams(
        tabelle_path="data/zweite_liga_tabelle_2025-04-20_16-18-22.csv",
        spiele_path="data/paarungen_ab_spieltag_31_2025-04-20_16-18-23.csv",
        anzahl=1000000,
        export=True,
    )
