"""
Tests for the scraping functions
"""

from scrape_league import get_current_table, get_fixtures, get_matchday_results


def test_get_current_table_defaut():
    """
    Test the get_current_table function using the default league.
    """
    table = get_current_table()

    # Check if the table is a list of dictionaries
    assert isinstance(table, list), "Table should be a list."
    assert all(
        isinstance(row, dict) for row in table
    ), "Each row should be a dictionary."

    # Check if the first row has the expected keys
    expected_keys = [
        "Platz",
        "Team",
        "Spiele",
        "Siege",
        "Unentschieden",
        "Niederlagen",
        "Tore",
        "Differenz",
        "Punkte",
    ]
    assert all(
        key in table[0] for key in expected_keys
    ), f"Expected keys not found in the first row: {expected_keys}"
    assert len(table) > 0, "Table should not be empty."


def test_get_current_table_custom():
    """
    Test the get_current_table function with a custom league.
    """
    table = get_current_table(league="premier-league")

    # Check if the table is a list of dictionaries
    assert isinstance(table, list), "Table should be a list."
    assert all(
        isinstance(row, dict) for row in table
    ), "Each row should be a dictionary."

    # Check if the first row has the expected keys
    expected_keys = [
        "Platz",
        "Team",
        "Spiele",
        "Siege",
        "Unentschieden",
        "Niederlagen",
        "Tore",
        "Differenz",
        "Punkte",
    ]
    assert all(
        key in table[0] for key in expected_keys
    ), f"Expected keys not found in the first row: {expected_keys}"
    assert len(table) > 0, "Table should not be empty."


def test_get_fixtures_defaut():
    """
    Test the get_fixtures function using the default league.
    """
    fixtures = get_fixtures(start_matchday=32)

    # Check if the fixtures are a list of dictionaries
    assert isinstance(fixtures, list), "Fixtures should be a list."
    assert all(
        isinstance(row, dict) for row in fixtures
    ), "Each fixture should be a dictionary."

    # Check if the first fixture has the expected keys
    expected_keys = ["Spieltag", "Paarungen"]
    assert all(
        key in fixtures[0] for key in expected_keys
    ), f"Expected keys not found in the first fixture: {expected_keys}"
    assert len(fixtures) > 0, "Fixtures should not be empty."


def test_get_fixtures_custom():
    """
    Test the get_fixtures function with a custom league.
    """
    fixtures = get_fixtures(start_matchday=36, end_matchday=37, league="premier-league")

    # Check if the fixtures are a list of dictionaries
    assert isinstance(fixtures, list), "Fixtures should be a list."
    assert all(
        isinstance(row, dict) for row in fixtures
    ), "Each fixture should be a dictionary."

    # Check if the first fixture has the expected keys
    expected_keys = ["Spieltag", "Paarungen"]
    assert all(
        key in fixtures[0] for key in expected_keys
    ), f"Expected keys not found in the first fixture: {expected_keys}"
    assert len(fixtures) > 0, "Fixtures should not be empty."


def test_get_matchday_results_defaut():
    """
    Test the get_matchday_results function using the default league.
    """
    results = get_matchday_results(start_matchday=1, end_matchday=2)

    # Check if the results are a list of dictionaries
    assert isinstance(results, list), "Results should be a list."
    assert all(
        isinstance(row, dict) for row in results
    ), "Each result should be a dictionary."

    # Check if the first result has the expected keys
    expected_keys = ["Spieltag", "Ergebnisse"]
    assert all(
        key in results[0] for key in expected_keys
    ), f"Expected keys not found in the first result: {expected_keys}"
    assert len(results) > 0, "Results should not be empty."


def test_get_matchday_results_custom():
    """
    Test the get_matchday_results function with a custom league.
    """
    results = get_matchday_results(
        start_matchday=1, end_matchday=2, league="premier-league"
    )

    # Check if the results are a list of dictionaries
    assert isinstance(results, list), "Results should be a list."
    assert all(
        isinstance(row, dict) for row in results
    ), "Each result should be a dictionary."

    # Check if the first result has the expected keys
    expected_keys = ["Spieltag", "Ergebnisse"]
    assert all(
        key in results[0] for key in expected_keys
    ), f"Expected keys not found in the first result: {expected_keys}"
    assert len(results) > 0, "Results should not be empty."
