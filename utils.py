"""
This module contains various utility functions that are used throughout the project.
"""

import os
import csv
import datetime
import ast


def export_data(data, filename_prefix):
    """
    Export data to a CSV file with a timestamp in the filename.
    Args:
        data (list): The data to export.
        filename_prefix (str): The prefix for the filename.
    """
    # Stelle sicher, dass der "data"-Ordner existiert
    os.makedirs("data", exist_ok=True)

    # Erzeuge einen Dateinamen mit Zeitstempel
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = os.path.join("data", filename)

    # Prüfe, ob die Datenliste leer ist
    if not data:
        print(f"Keine Daten zum Exportieren für {filename_prefix}.")
        return

    # Tabellen-Daten: Liste von Dictionaries
    if isinstance(data[0], dict):
        keys = data[0].keys()
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    # Spielpaarungen-Daten: Liste von Dicts mit Spieltag & Paarungen
    elif isinstance(data[0], (list, str, tuple)):
        # Fallback falls kein Dictionary übergeben wurde
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

    print(f"Daten erfolgreich exportiert nach {filepath}")


def read_csv_table(filepath):
    """
    Liest eine CSV-Datei ein und gibt eine Liste von Dictionaries zurück.
    Args:
        filepath (str): Der Pfad zur CSV-Datei.
    Returns:
        list: Eine Liste von Dictionaries, die die Daten der CSV-Datei repräsentieren.
    """
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extract_pairings_from_fixture_data(fixture_data):
    """
    Extrahiert Spielpaarungen aus einer Liste von Dictionaries im Format:
    [{'Spieltag': xx, 'Paarungen': [[Heim, Auswärts], ...]}, ...]
    Args:
        fixture_data (list): Liste von Dictionaries mit Spieltag und Paarungen.
    Returns:
        list: Liste von (Heim, Auswärts)-Tuplen.
    """
    pairings = []
    for spieltag in fixture_data:
        raw_matches = spieltag.get("Paarungen", [])
        for match in raw_matches:
            if isinstance(match, (list, tuple)) and len(match) == 2:
                heim, auswaerts = match[0].strip(), match[1].strip()
                pairings.append((heim, auswaerts))
    return pairings


def read_csv_fixtures(filepath):
    """
    Liest eine CSV-Datei mit Spielpaarungen ein und gibt eine Liste von Tuplen zurück.
    Args:
        filepath (str): Der Pfad zur CSV-Datei.
    Returns:
        list: Eine Liste von (Heim, Auswärts)-Tuplen.
    """
    fixture_data = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairings_str = row.get("Paarungen")
            spieltag = row.get("Spieltag")
            if pairings_str:
                try:
                    pairings = ast.literal_eval(pairings_str)
                    fixture_data.append(
                        {
                            "Spieltag": (
                                int(spieltag)
                                if spieltag and spieltag.isdigit()
                                else None
                            ),
                            "Paarungen": pairings,
                        }
                    )
                except (ValueError, SyntaxError):
                    print(f"Fehler beim Parsen von Paarungen: {pairings_str}")

    return extract_pairings_from_fixture_data(fixture_data)


def normalize_results(results_raw):
    """
    Bringt Rohdaten aus CSV oder Scraper in ein einheitliches Format.
    Args:
        results_raw (list of dict): Entweder direkt gescrapte Ergebnisse oder aus CSV.
    Returns:
        list of dict: Eine Liste mit vereinheitlichten Spielergebnissen.
    """
    normalized = []

    for row in results_raw:
        spieltag = int(row["Spieltag"])
        # Prüfen, ob "Ergebnisse" ein String ist (CSV) oder schon als Liste vorliegt (Scraper)
        spiele = (
            ast.literal_eval(row["Ergebnisse"])
            if isinstance(row["Ergebnisse"], str)
            else row["Ergebnisse"]
        )

        for spiel in spiele:
            heim, auswaerts, tore_heim, tore_auswaerts = spiel
            normalized.append(
                {
                    "Spieltag": spieltag,
                    "Heim": heim,
                    "Auswaerts": auswaerts,
                    "Tore_Heim": int(tore_heim),
                    "Tore_Auswaerts": int(tore_auswaerts),
                }
            )

    return normalized


def read_csv_results(filepath):
    """
    Liest eine CSV-Datei mit Spielergebnissen ein und gibt eine Liste aller Spiele zurück.
    Args:
        filepath (str): Der Pfad zur CSV-Datei
    Returns:
        list of dict: Eine Liste mit Dictionaries für jedes Spiel.
    """
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_results = list(reader)

    return normalize_results(raw_results)
