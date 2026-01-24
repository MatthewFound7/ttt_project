from typing import Callable

import pytest

import ttt_ui.views.stats as stats_view
from tests.unit.ttt_ui.views.fakes import FakeWidget


@pytest.fixture
def mock_stats_ui(monkeypatch: pytest.MonkeyPatch) -> None:
    import ttt_ui.views.stats as stats_view

    monkeypatch.setattr(stats_view, "CTkButton", FakeWidget)
    monkeypatch.setattr(stats_view, "CTkLabel", FakeWidget)
    monkeypatch.setattr(stats_view, "CTkFrame", FakeWidget)


@pytest.fixture
def close_handler(make_handler: Callable) -> Callable:
    return make_handler()


@pytest.fixture
def view(
    mock_stats_ui: None,
    close_handler: Callable,
) -> stats_view.StatsView:
    view = stats_view.StatsView(master=None, on_close=close_handler)

    view.placed = False

    def fake_place(**kwargs) -> None:
        view.placed = True
        view.place_args = kwargs

    def fake_place_forget() -> None:
        view.placed = False

    view.place = fake_place
    view.place_forget = fake_place_forget

    return view


def test_show_stats_places_all_widgets(view: stats_view.StatsView) -> None:
    view.show_stats(5, 0.5)

    assert view.placed is True
    assert view._close.placed is True
    assert view._title.placed is True
    assert view._player_title.placed is True
    assert view._player_score.placed is True
    assert view._player_over_total.placed is True


def test_show_stats_sets_text_values(view: stats_view.StatsView) -> None:
    view.show_stats(3, 0.25)

    assert view._player_score.text == "3"
    assert view._player_over_total.text == "(25.0%)"


def test_hide_stats_removes_view(view: stats_view.StatsView) -> None:
    view.show_stats(1, 0.1)
    view.hide_stats()

    assert view.placed is False
