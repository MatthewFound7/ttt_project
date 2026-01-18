from typing import Optional


class TicTacToeEnvironment:
    def __init__(self):
        self.reset()

    def reset(self) -> str:
        self.board = [" "] * 9
        self.current_player = "X"
        self.is_done = False
        self.winner = None
        return self.get_state()

    def get_state(self) -> str:
        return "".join(self.board)

    def legal_actions(self) -> list[int]:
        return [index for index, cell in enumerate(self.board) if cell == " "]

    def step(self, action: int) -> tuple[str, float, bool]:
        """
        Apply 'action' for the current player, return (next_state, reward_for_X, done)
        """

        if self.is_done or action not in range(9) or self.board[action] != " ":
            raise ValueError("Invalid action")

        self.board[action] = self.current_player

        self.winner = self._check_winner()

        if self.winner or " " not in self.board:
            self.is_done = True

        reward = 0.0
        if self.is_done:
            if self.winner == "O":
                reward = +1.0
            elif self.winner == "X":
                reward = -1.0
            else:
                reward = 0.0

        if not self.is_done:
            self.current_player = "X" if self.current_player == "O" else "O"

        return self.get_state(), reward, self.is_done

    def _check_winner(self) -> Optional[str]:
        b = self.board

        win_lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for i, j, k in win_lines:
            if b[i] != " " and b[i] == b[j] == b[k]:
                return b[i]

        return None

    def render(self) -> None:
        b = self.board

        def cell(index):
            return b[index] if b[index] != " " else str(index)

        print(f"{cell(0)} | {cell(1)} | {cell(2)}")
        print("--+---+--")
        print(f"{cell(3)} | {cell(4)} | {cell(5)}")
        print("--+---+--")
        print(f"{cell(6)} | {cell(7)} | {cell(8)}")
