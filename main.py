"""
This script combines multiple functions of the league outcomes repository,
constituting the entire process of scraping and analyzing league data to simulate
league outcomes.
"""

from scrape_league import get_current_table, get_fixtures, get_matchday_results
from analyze_matchdays import analyze_goals_separated, berechne_gewichte
from utils import normalize_results, extract_pairings_from_fixture_data
from sim_season_all import simulate_season_for_all_teams

# USER INPUTS
LEAGUE = "bundesliga"  # league name as per the kicker URL, e.g. "bundesliga"
PLAYED_MATCHDAYS = 33  # last matchday that has been played (integer)
FINAL_MATCHDAY = 34  # last matchday of the season (integer)
SEASON = "2024-25"  # season string as per kicker URL, e.g. "2024-25"
SIMULATION_RUNS = 1000000  # number of simulation runs (integer)
EXPORT = True  # whether to export the resulting plot or not (boolean)


# Check if the inputs are valid
if not isinstance(PLAYED_MATCHDAYS, int) or PLAYED_MATCHDAYS < 1:
    raise ValueError("PLAYED_MATCHDAYS must be a positive integer.")
if not isinstance(FINAL_MATCHDAY, int) or FINAL_MATCHDAY < 1:
    raise ValueError("FINAL_MATCHDAY must be a positive integer.")
if FINAL_MATCHDAY <= PLAYED_MATCHDAYS:
    raise ValueError("FINAL_MATCHDAY must be greater than PLAYED_MATCHDAYS.")
if not isinstance(SEASON, str) or len(SEASON) != 7 or SEASON[4] != "-":
    raise ValueError("SEASON must be a string in the format 'YYYY-YY'.")
if not isinstance(SIMULATION_RUNS, int) or SIMULATION_RUNS < 1:
    raise ValueError("SIMULATION_RUNS must be a positive integer.")
if not isinstance(EXPORT, bool):
    raise ValueError("EXPORT must be a boolean value.")

# Check for warnings based on the inputs
if SIMULATION_RUNS > 1000000:
    print("Warning: A high number of simulation runs may take a long time to complete.")
if PLAYED_MATCHDAYS < 10:
    print(
        "Warning: A low number of played matchdays may not provide a reliable simulation."
    )

# Scrape already played matchday results
results_raw = get_matchday_results(
    1, PLAYED_MATCHDAYS, league=LEAGUE, season=SEASON, export=False
)

# Normalize the results
results = normalize_results(results_raw)

# Analyze the results
home_goals, away_goals, results_distribution = analyze_goals_separated(results)

# Get the goal distribution and weights for home and away teams
torverteilung = [
    0,
    1,
    2,
    3,
    4,
]  # Currently hardcoded, could be dynamic based on the data
torgewichte_heim = berechne_gewichte(home_goals)
torgewichte_auswaerts = berechne_gewichte(away_goals)

# Scrape the current table and fixtures
current_table = get_current_table(league=LEAGUE, export=False)
fixtures_raw = get_fixtures(
    PLAYED_MATCHDAYS + 1,
    end_matchday=FINAL_MATCHDAY,
    league=LEAGUE,
    season=SEASON,
    export=False,
)
fixtures = extract_pairings_from_fixture_data(fixtures_raw)

# Simulate the remaining matchdays and generate the heatmap
simulate_season_for_all_teams(
    tabelle_path=None,
    spiele_path=None,
    table_raw=current_table,
    fixtures=fixtures,
    runs=SIMULATION_RUNS,
    export=EXPORT,
    torverteilung=torverteilung,
    torgewichte_heim=torgewichte_heim,
    torgewichte_auswaerts=torgewichte_auswaerts,
)
