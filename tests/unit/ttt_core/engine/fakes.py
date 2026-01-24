from dataclasses import dataclass
from typing import Optional

from ttt_core.domain.board import Board
from ttt_core.domain.types import Mark
from ttt_core.engine.stats import Stats


@dataclass
class FakeMark:
    value: str


@dataclass
class FakeStatus:
    is_over: bool
    winner: Optional[FakeMark]


@dataclass
class FakeBoard:
    winner: Optional[Mark] = None
    draw: bool = False

    def place_mark(self, index: int, mark: Mark) -> None:
        self.last_index = index
        self.last_mark = mark

    def winner_mark(self) -> Optional[Mark]:
        return self.winner

    def is_draw(self) -> bool:
        return self.draw


class FakeGame:
    def __init__(self, board: Board, stats: Stats) -> None:
        self.board = board
        self.stats = stats
        self.current_move_mark = FakeMark("X")
        self.reset_called = False

    def apply_move(self, index: int) -> FakeStatus:
        self.board.cells[index] = self.current_move_mark.value
        return FakeStatus(is_over=False, winner=None)

    def reset_game(self) -> None:
        self.reset_called = True
        self.board = Board()
        self.current_move_mark = FakeMark("X")
