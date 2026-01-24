import pytest

from ttt_core.engine.engine import Engine
from ttt_core.engine.stats import Stats


@pytest.fixture
def stats() -> Stats:
    return Stats()


@pytest.fixture
def engine(stats: Stats) -> Engine:
    return Engine(stats=stats)


def test_expose_board_returns_live_board(engine: Engine) -> None:
    board = engine.expose_board

    assert board.cells == [""] * 9

    engine.index_move_and_update_status(0)

    assert board.cells[0] != ""


def test_attempts_increment_with_each_move(engine: Engine) -> None:
    first = engine.index_move_and_update_status(0)
    second = engine.index_move_and_update_status(1)

    assert first["attempts"] == 1
    assert second["attempts"] == 2


def test_reset_clears_board_and_attempts(engine: Engine) -> None:
    engine.index_move_and_update_status(0)
    engine.index_move_and_update_status(1)

    engine.reset_game()

    assert engine.expose_board.cells == [""] * 9
    assert engine.lock_selection() is False


def test_game_over_and_winner_detected(engine: Engine) -> None:
    # X wins across top row
    moves = [0, 3, 1, 4, 2]

    result = None
    for move in moves:
        result = engine.index_move_and_update_status(move)
        if result["game_over"]:
            break

    assert result is not None
    assert result["game_over"] is True
    assert result["winner"] == "X"
    assert result["win_line"] == (0, 1, 2)


def test_stats_increment_after_completed_game(engine: Engine, stats: Stats) -> None:
    # O wins down left column
    moves = [1, 0, 2, 3, 4, 6]

    result = None
    for move in moves:
        result = engine.index_move_and_update_status(move)
        if result["game_over"]:
            break

    assert result is not None
    assert result["game_over"] is True

    assert stats.total_games == 1
    assert stats.player_wins in (0, 1)


def test_lock_selection_after_first_attempt(engine: Engine) -> None:
    assert engine.lock_selection() is False

    engine.index_move_and_update_status(0)

    assert engine.lock_selection() is True


def test_win_line_none_when_no_winner(engine: Engine) -> None:
    result = engine.index_move_and_update_status(0)

    assert result["game_over"] is False
    assert result["win_line"] is None
