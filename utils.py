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
    # Stelle sicher, dass der "Data"-Ordner existiert
    os.makedirs("Data", exist_ok=True)

    # Erzeuge einen Dateinamen mit Zeitstempel
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = os.path.join("Data", filename)

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


def read_csv_fixtures(filepath):
    """
    Liest eine CSV-Datei mit Spielpaarungen ein und gibt eine Liste von Tuplen zurück.
    Args:
        filepath (str): Der Pfad zur CSV-Datei.
    Returns:
        list: Eine Liste von Tuplen, die die Spielpaarungen repräsentieren.
    """
    fixtures = []
    with open(filepath, newline="", encoding="utf-8") as f:
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
                    print(f"Fehler beim Parsen von Paarungen: {pairings_str}")
    return fixtures


def read_csv_results(filepath):
    """
    Liest eine CSV-Datei mit Spielergebnissen ein und gibt eine Liste aller Spiele zurück.
    Args:
        filepath (str): Der Pfad zur CSV-Datei
    Returns:
        list of dict: Eine Liste mit Dictionaries für jedes Spiel.
    """
    results = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            spieltag = int(row["Spieltag"])
            spiele = ast.literal_eval(row["Ergebnisse"])
            for spiel in spiele:
                heim, auswaerts, tore_heim, tore_auswaerts = spiel
                results.append(
                    {
                        "Spieltag": spieltag,
                        "Heim": heim,
                        "Auswaerts": auswaerts,
                        "Tore_Heim": int(tore_heim),
                        "Tore_Auswaerts": int(tore_auswaerts),
                    }
                )
    return results
