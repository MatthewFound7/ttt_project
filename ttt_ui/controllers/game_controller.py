from dataclasses import dataclass
from typing import Optional, Tuple

from ttt_core.ai.agents import QAgent, RandomAgent
from ttt_core.engine.engine import Engine
from ttt_core.engine.stats import Stats
from ttt_ui.services.layout import CELLS


@dataclass(frozen=True)
class MoveResult:
    placed_index: Optional[int]
    attempts: int
    game_over: bool
    winner: str
    win_line: Optional[Tuple[int, int, int]]


def coord_to_index(click_x: float, click_y: float) -> int:
    """Uses Squared Euclidean Distance"""
    distances = [
        (idx, (cell_x - click_x) ** 2 + (cell_y - click_y) ** 2)
        for idx, (cell_x, cell_y) in enumerate(CELLS)
    ]
    return min(distances, key=lambda t: t[1])[0]


class GameController:
    """Handles mode selection and delegates to engine facade."""

    def __init__(self) -> None:
        self._stats = Stats()
        self._engine = Engine(stats=self._stats)
        self._agent: Optional[object] = RandomAgent()

    def set_mode_multi(self) -> None:
        self._agent = None

    def set_mode_easy(self) -> None:
        self._agent = RandomAgent()

    def set_challenge_mode(self, model_path: str) -> None:
        self._agent = QAgent(model_path)

    def reset_game_engine(self) -> None:
        self._engine.reset_game()

    def current_shape(self) -> str:
        return self._engine.current_mark()

    def register_click_and_move(self, x: float, y: float) -> MoveResult:
        index = coord_to_index(x, y)

        raw_move_status = self._engine.index_move_and_update_status(index)

        return self._produce_move_result(raw_move_status)

    def register_ai_click_and_move(self) -> MoveResult:
        index = self._agent.choose_move(self._engine.expose_board)

        raw_move_status = self._engine.index_move_and_update_status(index)

        return self._produce_move_result(raw_move_status)

    def ai_should_move(self) -> bool:
        return self._agent is not None and self.current_shape() == "O"

    def lock_selection(self) -> bool:
        return self._engine.lock_selection()

    def hold_stats(self) -> Tuple[int, int, float]:
        wins = self._stats.player_wins
        games = self._stats.total_games

        return wins, games, self._stats.percent_wins()

    def _produce_move_result(self, raw: dict) -> dict:
        return MoveResult(
            placed_index=raw.get("placed_index"),
            attempts=int(raw.get("attempts", 0)),
            game_over=bool(raw.get("game_over", False)),
            winner=str(raw.get("winner") or ""),
            win_line=raw.get("win_line"),
        )
