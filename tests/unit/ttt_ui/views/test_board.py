from typing import Callable

import pytest

import ttt_ui.views.board as board
from tests.unit.ttt_ui.views.fakes import FakeCanvas, FakeWidget


@pytest.fixture
def mock_board_ui(monkeypatch: pytest.MonkeyPatch) -> None:
    import ttt_ui.views.board as board

    monkeypatch.setattr(board, "CTkButton", FakeWidget)
    monkeypatch.setattr(board, "CTkLabel", FakeWidget)
    monkeypatch.setattr(board, "CTkFrame", FakeWidget)
    monkeypatch.setattr(board, "CTkCanvas", FakeCanvas)

    monkeypatch.setattr(board, "board_grid_x", [0.25, 0.5, 0.75])
    monkeypatch.setattr(board, "board_grid_y", [0.25, 0.5, 0.75])


@pytest.fixture
def click_handler(make_handler: Callable) -> Callable:
    return make_handler()


@pytest.fixture
def view(
    mock_board_ui: None,
    click_handler: Callable,
) -> board.BoardView:
    return board.BoardView(master=None, on_cell_click=click_handler)


def test_draw_game_grid_creates_lines(view: board.BoardView) -> None:
    canvas = view._canvas
    assert len(canvas.lines) == 4


def test_create_click_grid_creates_buttons_and_mapping(view: board.BoardView) -> None:
    view.create_click_grid()

    assert len(view.active_board_buttons) == 9
    assert len(view.coord_button_map) == 9

    for coord, btn in view.coord_button_map.items():
        assert coord in view.coord_button_map
        assert btn in view.active_board_buttons


def test_destroy_click_grid_removes_buttons(view: board.BoardView) -> None:
    view.create_click_grid()
    view.destroy_click_grid()

    assert view.active_board_buttons == []
    assert view.coord_button_map == {}


def test_set_button_active_disables_buttons(view: board.BoardView) -> None:
    view.create_click_grid()
    view.set_button_active(False)

    for btn in view.active_board_buttons:
        assert btn.state == "disabled"


def test_remove_cell_button_prefers_mapped_button(view: board.BoardView) -> None:
    view.create_click_grid()
    (x, y), btn = next(iter(view.coord_button_map.items()))

    fallback = type(btn)()
    view.remove_cell_button(x, y, fallback)

    assert btn.destroyed is True
    assert fallback.destroyed is False


def test_remove_cell_button_uses_fallback_when_missing(view: board.BoardView) -> None:
    fallback = type(view._canvas)()

    view.remove_cell_button(99.0, 99.0, fallback)

    assert fallback.destroyed is True


def test_render_mark_creates_label_and_tracks_position(view: board.BoardView) -> None:
    view.render_mark(0.5, 0.5, object())

    assert len(view._placed_items) == 1
    assert len(view._placed_positions) == 1

    item, x, y = view._placed_positions[0]
    assert x == 0.5
    assert y == 0.5
    assert item.placed is True


def test_clear_all_marks_destroys_labels(view: board.BoardView) -> None:
    view.render_mark(0.5, 0.5, object())
    view.render_mark(0.25, 0.25, object())

    view.clear_all_marks()

    assert view._placed_items == []
    assert view._placed_positions == []


def test_button_disable_on_win_creates_overlay(view: board.BoardView) -> None:
    view.button_disable_on_win()

    assert len(view.highlight_board_buttons) == 9
    for btn in view.highlight_board_buttons:
        assert btn.state == "disabled"


def test_destroy_highlight_overlay_removes_buttons(view: board.BoardView) -> None:
    view.button_disable_on_win()
    view.destroy_highlight_overlay()

    assert view.highlight_board_buttons == []


def test_replace_marks_and_lift_repositions_items(view: board.BoardView) -> None:
    view.render_mark(0.5, 0.5, object())

    item, _, _ = view._placed_positions[0]
    view.replace_marks_and_lift()

    assert item.placed is True
    assert item.lifted is True
