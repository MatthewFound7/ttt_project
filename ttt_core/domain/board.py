from dataclasses import dataclass, field
from typing import List, Optional

from ttt_core.domain import rules
from ttt_core.domain.types import Mark


@dataclass
class Board:
    cells: List[str] = field(default_factory=lambda: [""] * 9)

    def place_mark(self, idx: int, mark: Mark) -> None:
        self.cells[idx] = mark.value

    def legal_moves(self) -> List[int]:
        return [idx for idx, value in enumerate(self.cells) if value == ""]

    def winner_mark(self) -> Optional[str]:
        won, mark, _ = rules.has_winner(self.cells)
        return Mark(mark) if won and mark else None

    def is_draw(self) -> bool:
        return rules.is_draw(self.cells)
