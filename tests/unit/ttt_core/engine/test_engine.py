import pytest

import ttt_core.engine.engine as engine_module


def test_engine_initial_state(engine):
    assert engine.lock_selection() is False
    assert engine.load_stats() is not None


def test_expose_board_returns_board(engine):
    board = engine.expose_board

    assert len(board.cells) == 9


def test_current_mark_returns_game_mark(engine):
    assert engine.current_mark() == "X"


def test_lock_selection_after_first_attempt(engine, monkeypatch):
    monkeypatch.setattr(
        engine_module,
        "has_winner",
        lambda cells: (False, None, None),
    )

    engine.index_move_and_update_status(0)

    assert engine.lock_selection() is True


@pytest.mark.parametrize("move_index", [0, 4, 8])
def test_index_move_and_update_status_structure(engine, monkeypatch, move_index):
    monkeypatch.setattr(
        engine_module,
        "has_winner",
        lambda cells: (False, None, None),
    )

    result = engine.index_move_and_update_status(move_index)

    assert result["placed_index"] == move_index
    assert result["attempts"] == 1
    assert result["game_over"] is False
    assert result["winner"] == ""
    assert result["win_line"] is None


def test_load_stats_returns_injected_stats(engine, stats):
    assert engine.load_stats() is stats
