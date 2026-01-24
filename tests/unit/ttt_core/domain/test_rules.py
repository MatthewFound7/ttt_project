from ttt_core.domain.rules import has_winner, is_draw


def test_has_winner_detects_row_win() -> None:
    cells = ["X", "X", "X", "", "", "", "", "", ""]

    has_win, winner, line = has_winner(cells)

    assert has_win is True
    assert winner == "X"
    assert line == (0, 1, 2)


def test_has_winner_detects_column_win() -> None:
    cells = ["O", "", "", "O", "", "", "O", "", ""]

    has_win, winner, line = has_winner(cells)

    assert has_win is True
    assert winner == "O"
    assert line == (0, 3, 6)


def test_has_winner_detects_diagonal_win() -> None:
    cells = ["X", "", "", "", "X", "", "", "", "X"]

    has_win, winner, line = has_winner(cells)

    assert has_win is True
    assert winner == "X"
    assert line == (0, 4, 8)


def test_has_winner_returns_false_when_no_winner() -> None:
    cells = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]

    has_win, winner, line = has_winner(cells)

    assert has_win is False
    assert winner is None
    assert line is None


def test_is_draw_returns_true_when_board_full() -> None:
    cells = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]

    result = is_draw(cells)

    assert result is True


def test_is_draw_returns_false_when_board_not_full() -> None:
    cells = ["X", "O", "X", "", "O", "O", "O", "X", "X"]

    result = is_draw(cells)

    assert result is False
