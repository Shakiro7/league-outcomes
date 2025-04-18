# Liga-Simulator – Platzierungswahrscheinlichkeiten der zweiten Fußball-Bundesliga berechnen

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

### Tabelle (`tabelle.csv`)

```csv
Platz,Team,Spiele,Siege,Unentschieden,Niederlagen,Tore,Differenz,Punkte
1,Team A,29,14,10,5,63:36,27,52
2,Team B,29,15,6,8,43:34,9,51
...
```

### Spiele (`spiele.csv`)

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
python sim_season_all.py
```

-> Zeigt eine Heatmap der Wahrscheinlichkeiten für alle Teams
-> Optionaler Export einer PNG-Datei

---

## 📅 Saisonverlauf: Wöchentliche Heatmaps

In dieser Sektion werden ab sofort die aktuellen Platzierungswahrscheinlichkeiten für jeden verbleibenden Spieltag der zweiten Fußball-Bundesliga dokumentiert. 

Die Platzierungswahrscheinlichkeiten werden dabei jeweils auf Basis von 1.000.000 Simulationen der verbleibenden Spieltage generiert. Zur Simulation der einzelnen Spiele wird dazu die Funktion "simulate_game_realgoals" aus dem "sim.py" Modul verwendet. Diese Funktion wählt sowohl für das Heim-, als auch das Auswärtsteam eine zufällige Toranzahl aus. Die Wahrscheinlichkeiten für die Auswahl einer bestimmten Toranzahl decken sich mit den Toranzahlen, die von allen Heim- bzw. Auswärtsteams der zweiten Fußball-Bundesliga bis einschließlich zum 29. Spieltag der Saisan 2024/25 erzielt wurden (z.B. Heimteams haben vom 1. bis zum 29. Spieltag beispielsweise 54-mal 0 Tore erzielt, wohingegen Auswärtsteams an diesen Spieltagen 76-mal 0 Tore erzielt haben). Bei den Wahrscheinlichkeiten für Toranzahlen wird somit nicht nach einzelnen Teams unterschieden.

Die Platzierungswahrscheinlichkeiten repräsentieren die relative Häufigkeit bestimmter Platzierungen eines Teams in den 1.000.000 simulierten Saisonverläufen.

Beispiel: Spieltag 30 stellt die Platzierungswahrscheinlichkeiten der Teams VOR der Austragung der Spiele des 30. Spieltags dar.

| Spieltag | Heatmap |
|----------|---------|
| 30       | [Heatmap anzeigen](output/platzierungsprobs_realgoals_2025-04-18_12-05-48.png) |
| 31       | *(Noch nicht verfügbar)* |
| 32       | *(Noch nicht verfügbar)* |
| 33       | *(Noch nicht verfügbar)* |
| 34       | *(Noch nicht verfügbar)* |

-> Die Visualisierung wird nach jedem Spieltag aktualisiert und als PNG eingebunden oder verlinkt.
