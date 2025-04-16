import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.kicker.de"

def get_current_table():
    url = f"{BASE_URL}/2-bundesliga/tabelle"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    table_data = []
    rows = soup.select("table tbody tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 10:
            team_data = {
                "position": int(cols[0].text.strip()),
                "team": cols[1].text.strip(),
                "matches": int(cols[2].text.strip()),
                "wins": int(cols[3].text.strip()),
                "draws": int(cols[4].text.strip()),
                "losses": int(cols[5].text.strip()),
                "goals_for": int(cols[6].text.strip().split(":")[0]),
                "goals_against": int(cols[6].text.strip().split(":")[1]),
                "goal_diff": int(cols[7].text.strip()),
                "points": int(cols[8].text.strip())
            }
            table_data.append(team_data)
    return table_data


def get_remaining_fixtures():
    url = f"{BASE_URL}/2-bundesliga/spieltag"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    fixtures = []
    matches = soup.select(".kick__v100-gameRow")

    for match in matches:
        teams = match.select(".kick__v100-gameCell--clubname")
        datetime_str = match.select_one("time")
        if len(teams) == 2 and datetime_str:
            home = teams[0].text.strip()
            away = teams[1].text.strip()
            match_time = datetime_str.get("datetime")

            fixtures.append({
                "home": home,
                "away": away,
                "datetime": match_time
            })
    return fixtures


if __name__ == "__main__":
    table = get_current_table()
    fixtures = get_remaining_fixtures()

    print("Aktuelle Tabelle:")
    for row in table:
        print(row)

    print("\nVerbleibende Spiele:")
    for match in fixtures:
        print(match)