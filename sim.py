"""
Simulationsmodul für die Simulation von Fußballspielen und Aktualisierung der Tabelle.
"""

import random


def simulate_game():
    """
    Simuliert ein Spiel zwischen zwei Teams und gibt die Tore zurück.
    Returns:
        tuple: Ein Tupel mit den Toren des Heim- und Auswärtsteams.
    """
    return random.randint(0, 3), random.randint(0, 3)


def simulate_game_realgoals():
    """
    Simuliert ein Spiel zwischen zwei Teams basierend auf 
    realistischeren Ergebniswahrscheinlichkeiten.
    Returns:
        tuple: Ein Tupel mit den Toren des Heim- und Auswärtsteams.
    """

    # Gewichtete Wahrscheinlichkeiten für Tore (z.B. 1 Tor häufiger als 3+ Tore)
    torverteilung = [0, 1, 2, 3, 4]  # mögliche Tore
    torgewichte_heim = [
        54 / 261,
        87 / 261,
        61 / 261,
        40 / 261,
        19 / 261,
    ]  # Gewichtungen für Heimtore
    torgewichte_auswaerts = [
        76 / 261,
        80 / 261,
        61 / 261,
        25 / 261,
        19 / 261,
    ]  # Gewichtungen für Auswärtstore

    tore_heim = random.choices(torverteilung, weights=torgewichte_heim, k=1)[0]
    tore_auswaerts = random.choices(torverteilung, weights=torgewichte_auswaerts, k=1)[0]

    return tore_heim, tore_auswaerts


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
