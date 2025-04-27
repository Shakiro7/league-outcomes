# Liga-Simulator – Wahrscheinlichkeiten für finale Platzierungen in Fußball-Ligen berechnen

Dieses Projekt simuliert den Verlauf einer laufenden Ligasaison basierend auf der aktuellen Tabelle und den verbleibenden Spielpaarungen. Es berechnet die Wahrscheinlichkeiten, mit denen ein Team auf einem bestimmten Tabellenplatz landet – entweder für ein einzelnes Team (via CLI) oder für alle Teams mit Visualisierung (als Heatmap).

---

## Features

- Simulation des Saisonendes mit realistischen Spielergebnissen
- Analyse der Platzierungswahrscheinlichkeiten
- CLI-Tool für einzelne Teams
- Heatmap-Visualisierung für alle Teams

---

## Installation

```bash
git clone https://github.com/Shakiro7/league-outcomes.git
cd league-outcomes
pip install -r requirements.txt
```

---

## Datenstruktur

### Tabelle (siehe z.B. `zweite_liga_tabelle_2025-04-16_18-53-38.csv`)

```csv
Platz,Team,Spiele,Siege,Unentschieden,Niederlagen,Tore,Differenz,Punkte
1,Team A,29,14,10,5,63:36,27,52
2,Team B,29,15,6,8,43:34,9,51
...
```

### Spiele (siehe z.B. `paarungen_ab_spieltag_30_2025-04-16_18-53-39.csv`)

```csv
Spieltag,Paarungen
30,"[['Team A', 'Team B'], ['Team C', 'Team D']]"
31,"[['Team A', 'Team C'], ['Team B', 'Team D']]"
...
```

---

## Nutzung

### 1. CLI: Einzelteam simulieren

```bash
python sim_season_cli.py
```

-> Gibt die Platzierungs-Wahrscheinlichkeiten für ein bestimmtes Team aus.

### 2. Skript: Alle Teams simulieren & visualisieren

```bash
python main.py
```

-> Zeigt eine Heatmap der Platzierungs-Wahrscheinlichkeiten für alle Teams einer durch den Benutzer gewählten Liga
-> Optionaler Export einer PNG-Datei

---

## 📅 Saisonverlauf: Wöchentliche Heatmaps

In dieser Sektion werden ab sofort die aktuellen Platzierungswahrscheinlichkeiten für jeden verbleibenden Spieltag der 1. und 2. Fußball-Bundesliga dokumentiert. 

Die Platzierungswahrscheinlichkeiten werden dabei jeweils auf Basis von 1.000.000 Simulationen der verbleibenden Spieltage generiert. Zur Simulation der einzelnen Spiele wird dazu die Funktion "simulate_game_realgoals" aus dem "sim.py" Modul verwendet. Diese Funktion wählt sowohl für das Heim-, als auch das Auswärtsteam eine zufällige Toranzahl aus. Die Wahrscheinlichkeiten für die Auswahl einer bestimmten Toranzahl decken sich mit den Toranzahlen, die von allen Heim- bzw. Auswärtsteams der 1. bzw. 2. Fußball-Bundesliga bis einschließlich zum vorherigen Spieltag der Saison 2024/25 erzielt wurden (in der 2. Bundesliga haben Heimteams vom 1. bis zum 29. Spieltag beispielsweise 54-mal 0 Tore erzielt, wohingegen Auswärtsteams an diesen Spieltagen 76-mal 0 Tore erzielt haben). Bei den simulierten Wahrscheinlichkeiten für Toranzahlen wird somit nicht nach einzelnen Teams unterschieden.

Die Platzierungswahrscheinlichkeiten repräsentieren die relative Häufigkeit bestimmter Platzierungen eines Teams in den 1.000.000 simulierten Saisonverläufen.

Info: Die Heatmaps stellen die Platzierungswahrscheinlichkeiten der Teams NACH der Austragung der Spiele des jeweiligen Spieltags dar.

### Platzierungswahrscheinlichkeiten der 1. Fußball Bundesliga

| Spieltag | Heatmap |
|----------|---------|
| 30       | [Heatmap anzeigen](output/bundesliga_platzierungsprobs_nach_spieltag_30_runs_1000000.png) |
| 31       | [Heatmap anzeigen](output/bundesliga_platzierungsprobs_nach_spieltag_31_runs_1000000.png) |
| 32       | *(Noch nicht verfügbar)* |
| 33       | *(Noch nicht verfügbar)* |

### Platzierungswahrscheinlichkeiten der 2. Fußball Bundesliga

| Spieltag | Heatmap |
|----------|---------|
| 29       | [Heatmap anzeigen](output/2-bundesliga_platzierungsprobs_nach_spieltag_29_runs_1000000.png) |
| 30       | [Heatmap anzeigen](output/2-bundesliga_platzierungsprobs_nach_spieltag_30_runs_1000000.png) |
| 31       | [Heatmap anzeigen](output/2-bundesliga_platzierungsprobs_nach_spieltag_31_runs_1000000.png) |
| 32       | *(Noch nicht verfügbar)* |
| 33       | *(Noch nicht verfügbar)* |

-> Die Visualisierungen werden nach jedem Spieltag aktualisiert und als PNG eingebunden oder verlinkt.
