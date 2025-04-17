"""
Scrape the current table and remaining fixtures from kicker.de for the 2. Bundesliga.
"""

import re
import requests
from bs4 import BeautifulSoup
from utils import export_data

BASE_URL = "https://www.kicker.de"


def get_current_table(export: bool = False):
    """
    Scrape the current table from kicker.de for the 2. Bundesliga.
    Args:
        export (bool): If True, export the data to a CSV file.
    Returns:
        list: A list of dictionaries containing the table data.
    """
    url = f"{BASE_URL}/2-bundesliga/tabelle"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        )
    }
    res = requests.get(url, headers=headers)
    print(f"Response Status Code: {res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")

    table_data = []
    table = soup.find(
        "table",
        class_="kick__table kick__table--ranking kick__table--alternate kick__table--resptabelle",
    )
    if not table:
        print("Table not found")
        return table_data

    rows = table.select("tbody tr")

    def extract_cell_text(td):
        # Prüfe, ob eine Desktop-Version existiert
        desktop_span = td.find("span", class_="kick__table--show-desktop")
        if desktop_span:
            return desktop_span.get_text(strip=True)
        return td.get_text(strip=True)

    for row in rows:
        cols = row.find_all("td")
        if not cols or len(cols) < 10:
            continue  # Skipp Header-Zeilen oder unvollständige Einträge

        try:
            platz = extract_cell_text(cols[0])
            team_name = extract_cell_text(cols[3])
            team_name = re.sub(r" \((A|N)\)$", "", team_name)  # Entferne "(A)" oder "(N)"
            spiele = extract_cell_text(cols[4])
            siege = extract_cell_text(cols[5])
            unentschieden = extract_cell_text(cols[6])
            niederlagen = extract_cell_text(cols[7])
            tore = extract_cell_text(cols[8])
            differenz = extract_cell_text(cols[9])
            punkte = extract_cell_text(cols[10])

            team_data = {
                "Platz": platz,
                "Team": team_name,
                "Spiele": spiele,
                "Siege": siege,
                "Unentschieden": unentschieden,
                "Niederlagen": niederlagen,
                "Tore": tore,
                "Differenz": differenz,
                "Punkte": punkte,
            }

            table_data.append(team_data)
        except Exception as e:
            print(f"Fehler beim Parsen einer Zeile: {e}")
            continue

    if export:
        export_data(table_data, "zweite_liga_tabelle")

    return table_data


def get_remaining_fixtures(start_matchday: int, export: bool = False):
    """
    Scrape the remaining fixtures from kicker.de for the 2. Bundesliga.
    Args:
        start_matchday (int): The matchday to start scraping from.
        export (bool): If True, export the data to a CSV file.
    Returns:
        list: A list of dictionaries containing the fixtures data.
    """

    fixtures = []

    for matchday in range(start_matchday, 35):
        url = f"{BASE_URL}/2-bundesliga/spieltag/2024-25/{matchday}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            )
        }

        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(
                f"Fehler beim Laden von Spieltag {matchday}: Status {res.status_code}"
            )
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        main_section = soup.find("main", class_="kick__data-grid__main")
        if not main_section:
            print(f"Keine Spieldaten für Spieltag {matchday} gefunden.")
            continue

        match_blocks = main_section.find_all(
            "div", class_="kick__v100-gameList kick__module-margin"
        )
        matchday_fixtures = []

        for block in match_blocks:
            game_cells = block.find_all(
                "div", class_="kick__v100-gameList__gameRow__gameCell"
            )
            for cell in game_cells:
                team_tags = cell.find_all("a", class_="kick__v100-gameCell__team")
                if len(team_tags) == 2:
                    team1 = team_tags[0].find(
                        "div", class_="kick__v100-gameCell__team__name"
                    )
                    team2 = team_tags[1].find(
                        "div", class_="kick__v100-gameCell__team__name"
                    )
                    if team1 and team2:
                        team_names = [
                            team1.get_text(strip=True),
                            team2.get_text(strip=True),
                        ]
                        matchday_fixtures.append(team_names)

        fixtures.append({"Spieltag": matchday, "Paarungen": matchday_fixtures})

    if export:
        export_data(fixtures, f"paarungen_ab_spieltag_{start_matchday}")

    return fixtures


if __name__ == "__main__":
    table = get_current_table(export=True)
    fixtures = get_remaining_fixtures(30, export=True)  # Beispiel: Spieltag 30

    print("Aktuelle Tabelle:")
    for row in table:
        print(row)

    print("\nVerbleibende Spiele:")
    for match in fixtures:
        print(match)
