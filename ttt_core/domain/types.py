from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Mark(str, Enum):
    X_MARK = "X"
    O_MARK = "O"


@dataclass(frozen=True)
class GameStatus:
    winner: Optional[Mark]
    is_draw: bool
    is_over: bool
