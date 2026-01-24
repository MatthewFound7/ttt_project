from typing import Callable

import pytest

from tests.unit.ttt_ui.views.fakes import FakeImage, FakeWidget


@pytest.fixture(autouse=True)
def reset_widget_counter() -> None:
    FakeWidget.placed_count = 0


@pytest.fixture
def make_handler() -> Callable[[], Callable]:
    def factory() -> Callable:
        calls = []

        def handler(*args, **kwargs) -> None:
            calls.append((args, kwargs))

        handler.calls = calls
        return handler

    return factory


@pytest.fixture
def mock_pil(monkeypatch: pytest.MonkeyPatch) -> FakeImage:
    import ttt_ui.views.sidebar as sidebar_view

    fake = FakeImage()
    monkeypatch.setattr(
        sidebar_view.Image,
        "open",
        lambda path: fake,
    )
    return fake
