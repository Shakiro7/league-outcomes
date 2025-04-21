"""
Scrape data such as the current table, remaining fixtures, and matchday results from kicker.de.
"""

import re
import requests
from bs4 import BeautifulSoup
from utils import export_data

BASE_URL = "https://www.kicker.de"


def get_current_table(league: str = "2-bundesliga", export: bool = False):
    """
    Scrape a current table from kicker.de for a given league.
    Args:
        league (str): The league to scrape. Naming according to the kicker url. 
        Default is "2-bundesliga".
        export (bool): If True, export the data to a CSV file.
    Returns:
        list: A list of dictionaries containing the table data.
    """
    url = f"{BASE_URL}/{league}/tabelle"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        )
    }
    try:
        res = requests.get(
            url, headers=headers, timeout=10
        )  # 10s for the server to respond
        if res.status_code != 200:
            print(f"Fehler beim Laden der Tabelle: Status {res.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("Timeout beim Laden der Tabelle")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Allgemeiner Fehler beim Laden der Tabelle: {e}")
        return []

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
            team_name = re.sub(
                r" \((A|N)\)$", "", team_name
            )  # Entferne "(A)" oder "(N)"
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
        except (IndexError, AttributeError, ValueError) as e:
            print(f"Fehler beim Parsen einer Zeile: {e}")
            continue

    if export:
        export_data(table_data, f"{league}_tabelle")

    return table_data


def get_fixtures(
    start_matchday: int,
    end_matchday: int = 34,
    league: str = "2-bundesliga",
    season: str = "2024-25",
    export: bool = False,
):
    """
    Scrape fixtures from kicker.de for a given league.
    Args:
        start_matchday (int): The matchday to start scraping from.
        end_matchday (int): The last matchday to scrape. Default is 34.
        league (str): The league to scrape. Naming according to the kicker url. 
        Default is "2-bundesliga".
        season (str): The season to scrape. Default is "2024-25".
        export (bool): If True, export the data to a CSV file.
    Returns:
        list: A list of dictionaries containing the fixtures data.
    """

    fixtures = []

    for matchday in range(start_matchday, end_matchday + 1):
        # Adjust the URL for the current season
        url = f"{BASE_URL}/{league}/spieltag/{season}/{matchday}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            )
        }

        try:
            res = requests.get(
                url, headers=headers, timeout=10
            )  # 10s for the server to respond
            if res.status_code != 200:
                print(
                    f"Fehler beim Laden von Spieltag {matchday}: Status {res.status_code}"
                )
                continue
        except requests.exceptions.Timeout:
            print(f"Timeout beim Laden von Spieltag {matchday}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Allgemeiner Fehler bei Spieltag {matchday}: {e}")
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
        export_data(
            fixtures,
            f"{season}_{league}_paarungen_spieltag_{start_matchday}_bis_{end_matchday}",
        )

    return fixtures


def get_matchday_results(
    start_matchday: int,
    end_matchday: int,
    league: str = "2-bundesliga",
    season: str = "2024-25",
    export: bool = False,
):
    """
    Scrape the matchday results from kicker.de for a given league.
    Args:
        start_matchday (int): The matchday to start scraping from.
        end_matchday (int): The matchday to end scraping at.
        league (str): The league to scrape. Naming according to the kicker url. 
        Default is "2-bundesliga".
        season (str): The season to scrape. Default is "2024-25".
        export (bool): If True, export the data to a CSV file.
    Returns:
        list: A list of dictionaries containing the matchday results data.
    """

    results = []

    for matchday in range(start_matchday, end_matchday + 1):
        url = f"{BASE_URL}/{league}/spieltag/{season}/{matchday}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            )
        }

        try:
            res = requests.get(
                url, headers=headers, timeout=10
            )  # 10s for the server to respond
            if res.status_code != 200:
                print(
                    f"Fehler beim Laden von Spieltag {matchday}: Status {res.status_code}"
                )
                continue
        except requests.exceptions.Timeout:
            print(f"Timeout beim Laden von Spieltag {matchday}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Allgemeiner Fehler bei Spieltag {matchday}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        main_section = soup.find("main", class_="kick__data-grid__main")
        if not main_section:
            print(f"Keine Spieldaten für Spieltag {matchday} gefunden.")
            continue

        match_blocks = main_section.find_all(
            "div", class_="kick__v100-gameList kick__module-margin"
        )
        matchday_results = []

        for block in match_blocks:
            game_cells = block.find_all(
                "div", class_="kick__v100-gameList__gameRow__gameCell"
            )
            for cell in game_cells:
                team_tags = cell.find_all("a", class_="kick__v100-gameCell__team")
                scores = cell.find_all(
                    "div", class_="kick__v100-scoreBoard__scoreHolder__score"
                )

                if len(team_tags) == 2 and len(scores) >= 2:
                    team1 = team_tags[0].find(
                        "div", class_="kick__v100-gameCell__team__name"
                    )
                    team2 = team_tags[1].find(
                        "div", class_="kick__v100-gameCell__team__name"
                    )
                    if team1 and team2:
                        game_results = [
                            team1.get_text(strip=True),
                            team2.get_text(strip=True),
                            scores[0].get_text(strip=True),
                            scores[1].get_text(strip=True),
                        ]
                        matchday_results.append(game_results)

        results.append({"Spieltag": matchday, "Ergebnisse": matchday_results})

    if export:
        export_data(
            results,
            f"{season}_{league}_ergebnisse_spieltag_{start_matchday}_bis_{end_matchday}",
        )

    return results


if __name__ == "__main__":
    tabelle = get_current_table(export=False)
    paarungen = get_fixtures(30, export=False)
    ergebnisse = get_matchday_results(28, 29, export=False)

    print("Aktuelle Tabelle:")
    for zeile in tabelle:
        print(zeile)

    print("\nVerbleibende Spiele:")
    for spiel in paarungen:
        print(spiel)

    print("\nErgebnisse der angegebenen Spieltage:")
    for spiel in ergebnisse:
        print(spiel)
