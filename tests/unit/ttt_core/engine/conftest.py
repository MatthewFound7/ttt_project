import pytest

import ttt_core.engine.engine as engine_module
from tests.unit.ttt_core.engine.fakes import FakeBoard, FakeGame
from ttt_core.domain.board import Board
from ttt_core.engine.engine import Engine
from ttt_core.engine.stats import Stats


@pytest.fixture
def fake_board():
    return FakeBoard()


@pytest.fixture
def stats() -> Stats:
    return Stats()


@pytest.fixture
def empty_board() -> Board:
    return Board()


@pytest.fixture
def partial_board() -> Board:
    board = Board()
    board.cells = ["X", "", "O", "", "", "", "", "", ""]
    return board


@pytest.fixture
def engine(stats: Stats, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(engine_module, "Game", FakeGame)

    return Engine(stats=stats)
