"""
Analyse der Tore und Ergebnisse in Fußballspielen.
"""

from collections import Counter
from utils import read_csv_results


def analyze_goals(results):
    """
    Analysiert die Tore und Ergebnisse der Spiele.
    Args:
        results (list): Liste der Spielergebnisse.
    Returns:
        einzeltore_counter (Counter): Zählt die Anzahl der Tore pro Team.
        ergebnis_counter (Counter): Zählt die Ergebnisse (Sieg, Niederlage, Unentschieden).
    """
    einzeltore_counter = Counter()
    ergebnis_counter = Counter()

    for spiel in results:
        tore_heim = spiel["Tore_Heim"]
        tore_auswaerts = spiel["Tore_Auswaerts"]

        # Einzelne Tore zählen (pro Team)
        einzeltore_counter[tore_heim] += 1
        einzeltore_counter[tore_auswaerts] += 1

        # Ergebnis (aus Sicht Heimteam)
        if tore_heim > tore_auswaerts:
            ergebnis_counter["Sieg"] += 1
        elif tore_heim < tore_auswaerts:
            ergebnis_counter["Niederlage"] += 1
        else:
            ergebnis_counter["Unentschieden"] += 1

    return einzeltore_counter, ergebnis_counter


def analyze_goals_separated(results):
    """
    Analysiert die Tore und Ergebnisse der Spiele getrennt für Heim- und Auswärtstore.
    Args:
        results (list): Liste der Spielergebnisse.
    Returns:
        heimtore_counter (Counter): Zählt die Anzahl der Heimtore.
        auswaertstore_counter (Counter): Zählt die Anzahl der Auswärtstore.
        ergebnis_counter (Counter): Zählt die Ergebnisse (Sieg, Niederlage, Unentschieden).
    """
    heimtore_counter = Counter()
    auswaertstore_counter = Counter()
    ergebnis_counter = Counter()

    for spiel in results:
        tore_heim = spiel["Tore_Heim"]
        tore_auswaerts = spiel["Tore_Auswaerts"]

        heimtore_counter[tore_heim] += 1
        auswaertstore_counter[tore_auswaerts] += 1

        if tore_heim > tore_auswaerts:
            ergebnis_counter["Sieg"] += 1
        elif tore_heim < tore_auswaerts:
            ergebnis_counter["Niederlage"] += 1
        else:
            ergebnis_counter["Unentschieden"] += 1

    return heimtore_counter, auswaertstore_counter, ergebnis_counter


def print_results(einzeltore_counter, ergebnis_counter):
    """
    Gibt die Ergebnisse der Tore und Spielergebnisse aus.
    Args:
        einzeltore_counter (Counter): Zählt die Anzahl der Tore pro Team.
        ergebnis_counter (Counter): Zählt die Ergebnisse (Sieg, Niederlage, Unentschieden).
    """
    print("Verteilung der erzielten Tore (je Mannschaft):")
    for tore in sorted(einzeltore_counter):
        print(f"{einzeltore_counter[tore]:>3}x {tore} Tor(e)")

    total = sum(ergebnis_counter.values())
    print("\n Verteilung der Spielergebnisse:")
    for ergebnis, anzahl in ergebnis_counter.items():
        prozent = anzahl / total * 100
        print(f"{ergebnis:<13}: {anzahl:>3} Spiele ({prozent:.2f}%)")


def print_results_separated(heimtore_counter, auswaertstore_counter, ergebnis_counter):
    """
    Gibt die Ergebnisse der Tore und Spielergebnisse getrennt für Heim- und Auswärtstore aus.
    Args:
        heimtore_counter (Counter): Zählt die Anzahl der Heimtore.
        auswaertstore_counter (Counter): Zählt die Anzahl der Auswärtstore.
        ergebnis_counter (Counter): Zählt die Ergebnisse (Sieg, Niederlage, Unentschieden).
    """
    print("Heimtore-Verteilung:")
    for tore in sorted(heimtore_counter):
        print(f"{heimtore_counter[tore]:>3}x {tore} Tor(e)")

    print("\n Auswärtstore-Verteilung:")
    for tore in sorted(auswaertstore_counter):
        print(f"{auswaertstore_counter[tore]:>3}x {tore} Tor(e)")

    total = sum(ergebnis_counter.values())
    print("\n Verteilung der Spielergebnisse:")
    for ergebnis, anzahl in ergebnis_counter.items():
        prozent = anzahl / total * 100
        print(f"{ergebnis:<13}: {anzahl:>3} Spiele ({prozent:.2f}%)")


def berechne_gewichte(
    counter,
):  # currently hardcoded for 0-4 goals; should be dynamic based on the data
    """
    Berechnet die Gewichtungen für Tore basierend auf der Verteilung.
    Args:
        counter (Counter): Zählt die Anzahl der Tore pro Team.
    Returns:
        list: Gewichtungen für Tore von 0 bis 4.
    """
    gewichte = [0] * 5
    for tore, anzahl in counter.items():
        if tore >= 4:
            gewichte[4] += anzahl
        else:
            gewichte[tore] += anzahl
    gesamt = sum(gewichte)
    return [wert / gesamt for wert in gewichte]


if __name__ == "__main__":
    DATEIPFAD = "data/ergebnisse_spieltag_1_bis_29.csv"
    ergebnisse = read_csv_results(DATEIPFAD)
    heimtore, auswaertstore, ergebnisse_verteilung = analyze_goals_separated(ergebnisse)
    print_results_separated(heimtore, auswaertstore, ergebnisse_verteilung)
    print("\nGewichtungen für Heimtore:")
    print(berechne_gewichte(heimtore))
    print("\nGewichtungen für Auswärtstore:")
    print(berechne_gewichte(auswaertstore))
