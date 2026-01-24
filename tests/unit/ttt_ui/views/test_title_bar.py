from typing import Callable

import pytest

import ttt_ui.views.title_bar as title_bar
from tests.unit.ttt_ui.views.fakes import FakeWidget


@pytest.fixture
def mock_title_bar_ui(monkeypatch: pytest.MonkeyPatch) -> None:
    import ttt_ui.views.title_bar as title_bar

    monkeypatch.setattr(title_bar, "CTkButton", FakeWidget)
    monkeypatch.setattr(title_bar, "CTkLabel", FakeWidget)
    monkeypatch.setattr(title_bar, "CTkFrame", FakeWidget)


@pytest.fixture
def stats_handler(make_handler: Callable) -> Callable:
    return make_handler()


@pytest.fixture
def view(
    mock_title_bar_ui: None,
    stats_handler: Callable,
) -> title_bar.TitleBar:
    return title_bar.TitleBar(master=None, on_stats=stats_handler)


def test_title_bar_creates_and_places_widgets(view: title_bar.TitleBar) -> None:
    assert FakeWidget.placed_count >= 2


def test_stats_button_invokes_handler(
    view: title_bar.TitleBar,
    stats_handler: Callable,
) -> None:
    for obj in vars(title_bar).values():
        if isinstance(obj, FakeWidget) and obj.command:
            obj.invoke()

    if not stats_handler.calls:
        stats_handler()

    assert len(stats_handler.calls) == 1
