from typing import Any, Dict

from ttt_core.domain.board import Board
from ttt_core.domain.rules import has_winner
from ttt_core.engine.game import Game
from ttt_core.engine.stats import Stats


class Engine:
    def __init__(self, stats: Stats) -> None:
        self.stats = stats
        self._game = Game(board=Board(), stats=stats)
        self._attempts = 0

    @property
    def expose_board(self) -> Board:
        return self._game.board

    def current_mark(self) -> str:
        return self._game.current_move_mark.value

    def lock_selection(self) -> bool:
        return self._attempts >= 1

    def reset_game(self) -> None:
        self._game.reset_game()
        self._attempts = 0

    def index_move_and_update_status(self, index: int) -> Dict[str, Any]:
        status = self._game.apply_move(index)
        self._attempts += 1

        cells = self._game.board.cells
        _, _, win_triple = has_winner(cells)

        return {
            "placed_index": index,
            "attempts": self._attempts,
            "game_over": status.is_over,
            "winner": status.winner.value if status.winner else "",
            "win_line": win_triple,
        }

    def load_stats(self) -> Stats:
        return self.stats
