from typing import Callable, Tuple

import pytest

import ttt_ui.views.sidebar as sidebar_view
from tests.unit.ttt_ui.views.fakes import FakeImage, FakeWidget


@pytest.fixture
def mock_sidebar_ui(monkeypatch: pytest.MonkeyPatch) -> None:
    import ttt_ui.views.sidebar as sidebar_view

    monkeypatch.setattr(sidebar_view, "CTkButton", FakeWidget)
    monkeypatch.setattr(sidebar_view, "CTkLabel", FakeWidget)
    monkeypatch.setattr(sidebar_view, "CTkFrame", FakeWidget)
    monkeypatch.setattr(sidebar_view, "CTkCanvas", FakeWidget)
    monkeypatch.setattr(sidebar_view, "CTkImage", FakeImage)


@pytest.fixture
def handlers(make_handler: Callable) -> Tuple[Callable, Callable, Callable, Callable, Callable]:
    return (
        make_handler(),
        make_handler(),
        make_handler(),
        make_handler(),
        make_handler(),
    )


@pytest.fixture
def view(
    mock_sidebar_ui: None,
    handlers: Tuple[Callable, Callable, Callable, Callable, Callable],
) -> sidebar_view.SidebarView:
    on_restart, on_multi, on_easy, on_hard, on_imp = handlers

    return sidebar_view.SidebarView(
        master=None,
        cross_menu=object(),
        circle_menu=object(),
        arrow_left=object(),
        on_restart=on_restart,
        on_multi=on_multi,
        on_easy=on_easy,
        on_hard=on_hard,
        on_impossible=on_imp,
    )


def test_highlight_mode_button_sets_border(view: sidebar_view.SidebarView) -> None:
    view.highlight_mode_button(view.easy_button)

    for btn in [
        view.easy_button,
        view.hard_button,
        view.imp_button,
        view.multi_button,
    ]:
        assert btn.border_color is not None

    assert view.easy_button.border_width == 3


def test_move_turn_arrow_positions_for_x(view: sidebar_view.SidebarView) -> None:
    view.move_turn_arrow("X")

    assert view._arrow_label.placed is True


def test_hide_turn_arrow_destroys_label(view: sidebar_view.SidebarView) -> None:
    view.hide_turn_arrow()

    assert view._arrow_label.destroyed is True


def test_reset_turn_arrow_recreates_label(view: sidebar_view.SidebarView) -> None:
    old_label = view._arrow_label
    view.reset_turn_arrow()

    assert old_label.destroyed is True
    assert view._arrow_label is not old_label
    assert view._arrow_label.placed is True


def test_clear_game_results_clears_all(view: sidebar_view.SidebarView) -> None:
    view._win_icon = FakeWidget()
    view.clear_game_results()

    assert view._win_icon is None
    assert view._play_again.placed is False


def test_show_game_results_draw(view: sidebar_view.SidebarView) -> None:
    view.show_game_results("", "fake/path.png", (32, 32))

    assert view._draw_result.placed is True
    assert view._play_again.placed is True


def test_show_game_results_win(
    view: sidebar_view.SidebarView,
    mock_pil,
) -> None:
    view.show_game_results("X", "fake/path.png", (64, 64))

    assert view._win_icon is not None
    assert view._play_again.placed is True


def test_enable_game_mode_selection(view: sidebar_view.SidebarView) -> None:
    view.disable_game_mode_selection()

    for btn in [
        view.multi_button,
        view.easy_button,
        view.hard_button,
        view.imp_button,
    ]:
        assert btn.state == "disabled"

    view.enable_game_mode_selection()

    for btn in [
        view.multi_button,
        view.easy_button,
        view.hard_button,
        view.imp_button,
    ]:
        assert btn.state == "normal"
