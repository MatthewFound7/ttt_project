import pytest

from ttt_core.domain.types import Mark
from ttt_core.engine.game import Game


@pytest.fixture
def game(fake_board, stats):
    return Game(board=fake_board, stats=stats)


def test_apply_move_places_mark(game, fake_board):
    game.apply_move(3)

    assert fake_board.last_index == 3
    assert fake_board.last_mark == Mark.X_MARK


def test_apply_move_toggles_mark_when_no_win_or_draw(game):
    game.apply_move(0)

    assert game.current_move_mark == Mark.O_MARK
    assert game.game_over is False


@pytest.mark.parametrize(
    "winner,expected_player_wins",
    [
        (Mark.X_MARK, 1),
        (Mark.O_MARK, 0),
    ],
)
def test_apply_move_when_winner_ends_game_and_records_stats(
    fake_board,
    stats,
    winner,
    expected_player_wins,
):
    fake_board.winner = winner
    game = Game(board=fake_board, stats=stats)

    status = game.apply_move(1)

    assert status.is_over is True
    assert status.winner == winner
    assert stats.total_games == 1
    assert stats.player_wins == expected_player_wins
    assert game.game_over is True


def test_apply_move_when_draw_ends_game_and_records_stats(
    fake_board,
    stats,
):
    fake_board.draw = True
    game = Game(board=fake_board, stats=stats)

    status = game.apply_move(5)

    assert status.is_over is True
    assert status.is_draw is True
    assert status.winner is None
    assert stats.total_games == 1
    assert stats.player_wins == 0
    assert game.game_over is True


def test_reset_game_resets_state(game, fake_board):
    game.apply_move(0)

    game.reset_game()

    assert game.current_move_mark == Mark.X_MARK
    assert game.game_over is False
