import pytest

from ttt_core.engine.stats import Stats


def test_initial_values(stats):
    assert stats.player_wins == 0
    assert stats.total_games == 0
    assert stats.percent_wins() == 0.0


def test_record_game_increments_total_games(stats):
    stats.record_game()

    assert stats.total_games == 1


def test_record_player_win_increments_player_wins(stats):
    stats.record_player_win()

    assert stats.player_wins == 1


@pytest.mark.parametrize(
    "wins,games,expected_percent",
    [
        (0, 1, 0.0),
        (1, 1, 1.0),
        (1, 2, 0.5),
        (2, 4, 0.5),
        (3, 4, 0.75),
    ],
)
def test_percent_wins_calculation(wins, games, expected_percent):
    stats = Stats(player_wins=wins, total_games=games)

    assert stats.percent_wins() == expected_percent
