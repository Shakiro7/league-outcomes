"""
Tests for the game simulations module.
"""

# Import the functions to be tested from the folder one level above
from sim import simulate_game_realgoals, simulate_game_randint


def test_simulate_game_realgoals_default():
    """
    Test the simulate_game_realgoals function with default parameters.
    """
    # Simulate a game with default parameters
    home_goals, away_goals = simulate_game_realgoals()

    # Check that the goals are within the expected range
    assert 0 <= home_goals <= 4, "Home goals out of expected range."
    assert 0 <= away_goals <= 4, "Away goals out of expected range."
    assert isinstance(home_goals, int), "Home goals should be an integer."
    assert isinstance(away_goals, int), "Away goals should be an integer."


def test_simulate_game_realgoals_custom():
    """
    Test the simulate_game function with custom parameters.
    """
    # Custom parameters for simulation
    torverteilung = [0, 1, 2, 3, 4]
    torgewichte_heim = [0.1, 0.3, 0.4, 0.15, 0.05]
    torgewichte_auswaerts = [0.05, 0.15, 0.4, 0.3, 0.1]

    # Simulate a game with custom parameters
    home_goals, away_goals = simulate_game_realgoals(
        torverteilung, torgewichte_heim, torgewichte_auswaerts
    )

    # Check that the goals are within the expected range
    assert 0 <= home_goals <= 4, "Home goals out of expected range."
    assert 0 <= away_goals <= 4, "Away goals out of expected range."
    assert isinstance(home_goals, int), "Home goals should be an integer."
    assert isinstance(away_goals, int), "Away goals should be an integer."


def test_simulate_game_randint():
    """
    Test the simulate_game_randint function with custom parameters.
    """
    # Custom parameters for simulation
    tore_heim_min = 0
    tore_heim_max = 3
    tore_auswaerts_min = 0
    tore_auswaerts_max = 3

    # Simulate a game with custom parameters
    home_goals, away_goals = simulate_game_randint(
        tore_heim_min, tore_heim_max, tore_auswaerts_min, tore_auswaerts_max
    )

    # Check that the goals are within the expected range
    assert (
        tore_heim_min <= home_goals <= tore_heim_max
    ), "Home goals out of expected range."
    assert (
        tore_auswaerts_min <= away_goals <= tore_auswaerts_max
    ), "Away goals out of expected range."
    assert isinstance(home_goals, int), "Home goals should be an integer."
    assert isinstance(away_goals, int), "Away goals should be an integer."
