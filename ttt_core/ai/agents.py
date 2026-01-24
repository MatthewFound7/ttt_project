import pickle
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Tuple

from ttt_core.domain.board import Board


@dataclass
class QAgent:
    q_path: str
    q_values_load: DefaultDict[Tuple[str, int], float] = None

    def __post_init__(self) -> None:
        """Load Q-table into defaultdict."""

        with open(self.q_path, "rb") as handle:
            loaded = pickle.load(handle)

        self.q_values_load = defaultdict(float, loaded)

    def choose_best_move(self, board: Board) -> int:
        """Return best legal move using greedy Q-values."""

        state = self._board_state(board)
        legal_moves = board.legal_moves()

        q_values = [(idx, self.q_values_load[(state, idx)]) for idx in legal_moves]

        max_value = max(q_val for _, q_val in q_values)
        best_move = [idx for idx, q_val in q_values if q_val == max_value]

        return random.choice(best_move)

    def _board_state(self, board: Board) -> str:
        state_cells = board.cells

        return "".join(cell if cell else " " for cell in state_cells)


@dataclass(frozen=True)
class RandomAgent:
    def choose_random_move(self, board: Board) -> int:
        """Chooses a random legal move index."""
        legal = board.legal_moves()

        return random.choice(legal)
