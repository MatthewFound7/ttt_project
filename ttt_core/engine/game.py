from dataclasses import dataclass

from ttt_core.domain.board import Board
from ttt_core.domain.types import GameStatus, Mark
from ttt_core.engine.stats import Stats


@dataclass
class Game:
    """Runs turns and evaluates game outcome."""

    board: Board
    stats: Stats
    current_move_mark: Mark = Mark.X_MARK
    game_over: bool = False

    def apply_move(self, index: int) -> GameStatus:
        self.board.place_mark(index, self.current_move_mark)
        winner = self.board.winner_mark()
        draw = self.board.is_draw()

        if winner or draw:
            self.game_over = True
            self.stats.record_game()
            if winner == Mark.X_MARK:
                self.stats.record_player_win()
            return GameStatus(winner=winner, is_draw=draw, is_over=True)

        self.current_move_mark = (
            Mark.O_MARK if self.current_move_mark == Mark.X_MARK else Mark.X_MARK
        )
        return GameStatus(winner=None, is_draw=False, is_over=False)

    def reset_game(self) -> None:
        self.board.cells = [""] * 9
        self.current_move_mark = Mark.X_MARK
        self.game_over = False
