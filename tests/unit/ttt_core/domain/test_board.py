from ttt_core.domain.board import Board
from ttt_core.domain.types import Mark


def test_place_mark_sets_cell_value() -> None:
    board = Board()
    index = 4

    board.place_mark(index, Mark.X_MARK)

    assert board.cells[index] == Mark.X_MARK.value


def test_legal_moves_returns_all_empty_indices_initially() -> None:
    board = Board()

    moves = board.legal_moves()

    assert moves == list(range(9))


def test_legal_moves_excludes_filled_cells() -> None:
    board = Board()
    board.place_mark(0, Mark.X_MARK)
    board.place_mark(4, Mark.O_MARK)

    moves = board.legal_moves()

    assert 0 not in moves
    assert 4 not in moves
    assert len(moves) == 7


def test_winner_mark_returns_none_when_no_winner() -> None:
    board = Board()
    board.cells = ["X", "O", "X", "X", "O", "O", "O", "X", ""]

    winner = board.winner_mark()

    assert winner is None


def test_winner_mark_returns_mark_when_winner_exists() -> None:
    board = Board()
    board.cells = ["X", "X", "X", "", "", "", "", "", ""]

    winner = board.winner_mark()

    assert winner == Mark.X_MARK
