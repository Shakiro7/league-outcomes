from collections import Counter
from utils import read_csv_results


def analyze_goals(results):
    einzeltore_counter = Counter()
    ergebnis_counter = Counter()

    for spiel in results:
        tore_heim = spiel["Tore_Heim"]
        tore_auswärts = spiel["Tore_Auswärts"]

        # Einzelne Tore zählen (pro Team)
        einzeltore_counter[tore_heim] += 1
        einzeltore_counter[tore_auswärts] += 1

        # Ergebnis (aus Sicht Heimteam)
        if tore_heim > tore_auswärts:
            ergebnis_counter["Sieg"] += 1
        elif tore_heim < tore_auswärts:
            ergebnis_counter["Niederlage"] += 1
        else:
            ergebnis_counter["Unentschieden"] += 1

    return einzeltore_counter, ergebnis_counter


def analyze_goals_separated(results):
    heimtore_counter = Counter()
    auswärtstore_counter = Counter()
    ergebnis_counter = Counter()

    for spiel in results:
        tore_heim = spiel["Tore_Heim"]
        tore_auswärts = spiel["Tore_Auswärts"]

        heimtore_counter[tore_heim] += 1
        auswärtstore_counter[tore_auswärts] += 1

        if tore_heim > tore_auswärts:
            ergebnis_counter["Sieg"] += 1
        elif tore_heim < tore_auswärts:
            ergebnis_counter["Niederlage"] += 1
        else:
            ergebnis_counter["Unentschieden"] += 1

    return heimtore_counter, auswärtstore_counter, ergebnis_counter


def print_results(einzeltore_counter, ergebnis_counter):
    print("Verteilung der erzielten Tore (je Mannschaft):")
    for tore in sorted(einzeltore_counter):
        print(f"{einzeltore_counter[tore]:>3}x {tore} Tor(e)")

    total = sum(ergebnis_counter.values())
    print("\n Verteilung der Spielergebnisse:")
    for ergebnis, anzahl in ergebnis_counter.items():
        prozent = anzahl / total * 100
        print(f"{ergebnis:<13}: {anzahl:>3} Spiele ({prozent:.2f}%)")


def print_results_separated(heimtore_counter, auswärtstore_counter, ergebnis_counter):
    print("Heimtore-Verteilung:")
    for tore in sorted(heimtore_counter):
        print(f"{heimtore_counter[tore]:>3}x {tore} Tor(e)")

    print("\n Auswärtstore-Verteilung:")
    for tore in sorted(auswärtstore_counter):
        print(f"{auswärtstore_counter[tore]:>3}x {tore} Tor(e)")

    total = sum(ergebnis_counter.values())
    print("\n Verteilung der Spielergebnisse:")
    for ergebnis, anzahl in ergebnis_counter.items():
        prozent = anzahl / total * 100
        print(f"{ergebnis:<13}: {anzahl:>3} Spiele ({prozent:.2f}%)")


if __name__ == "__main__":
    dateipfad = "Data/ergebnisse_spieltag_1_bis_29.csv"
    ergebnisse = read_csv_results(dateipfad)
    heimtore, auswärtstore, ergebnisse_verteilung = analyze_goals_separated(ergebnisse)
    print_results_separated(heimtore, auswärtstore, ergebnisse_verteilung)    