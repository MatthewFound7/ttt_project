from dataclasses import dataclass


@dataclass
class Stats:
    player_wins: int = 0
    total_games: int = 0

    def record_player_win(self) -> None:
        self.player_wins += 1

    def record_game(self) -> None:
        self.total_games += 1

    def percent_wins(self):
        return (self.player_wins / self.total_games) if self.total_games else 0.0
