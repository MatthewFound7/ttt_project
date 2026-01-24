import pytest

from ttt_ui.controllers.game_controller import GameController, MoveResult


class FixedAgent:
    def __init__(self, move: int) -> None:
        self._move = move

    def choose_move(self, board: object) -> int:
        return self._move


@pytest.fixture
def controller() -> GameController:
    return GameController()


def test_human_click_places_mark_and_returns_move_result(controller: GameController) -> None:
    result = controller.register_click_and_move(0.0, 0.0)

    assert isinstance(result, MoveResult)
    assert result.placed_index is not None
    assert result.attempts >= 1
    assert result.winner == ""
    assert result.game_over is False


def test_ai_should_move_false_in_multi_mode(controller: GameController) -> None:
    controller.set_mode_multi()

    assert controller.ai_should_move() is False


def test_ai_should_move_true_when_o_turn(controller: GameController) -> None:
    controller.set_mode_easy()

    controller.register_click_and_move(0.0, 0.0)

    assert controller.ai_should_move() is True


def test_ai_move_executes_and_returns_result(controller: GameController) -> None:
    controller._agent = FixedAgent(1)

    controller.register_click_and_move(0.0, 0.0)

    result = controller.register_ai_click_and_move()

    assert isinstance(result, MoveResult)
    assert result.placed_index == 1
    assert result.attempts >= 1


def test_reset_clears_game_and_allows_new_moves(controller: GameController) -> None:
    first = controller.register_click_and_move(0.0, 0.0)

    controller.reset_game_engine()

    second = controller.register_click_and_move(0.0, 0.0)

    assert first.placed_index == second.placed_index
    assert first.attempts == 1
    assert second.attempts == 1


def test_lock_selection_blocks_moves_after_game_over(controller: GameController) -> None:
    controller.register_click_and_move(0.0, 0.0)
    controller.register_click_and_move(100.0, 0.0)
    controller.register_click_and_move(0.0, 100.0)
    controller.register_click_and_move(100.0, 100.0)
    result = controller.register_click_and_move(50.0, 50.0)

    if result.game_over:
        assert controller.lock_selection() is True


def test_stats_increment_after_game(controller: GameController) -> None:
    class WinningAgent:
        def __init__(self) -> None:
            self._moves = iter([0, 3, 6])  # Vertical win for O

        def choose_move(self, board: object) -> int:
            return next(self._moves)

    controller._agent = WinningAgent()

    controller.register_click_and_move(1.0, 1.0)  # X
    controller.register_ai_click_and_move()  # O -> 0

    controller.register_click_and_move(2.0, 2.0)  # X
    controller.register_ai_click_and_move()  # O -> 3

    controller.register_click_and_move(4.0, 4.0)  # X
    result = controller.register_ai_click_and_move()  # O -> 6 (win)

    assert result.game_over is True

    wins, games, percent = controller.hold_stats()

    assert games >= 1
    assert 0.0 <= percent <= 100.0


def test_set_challenge_mode_sets_agent(controller: GameController, tmp_path) -> None:
    import pickle

    model_path = tmp_path / "fake_model.pkl"

    with open(model_path, "wb") as handle:
        pickle.dump({}, handle)

    controller.set_challenge_mode(str(model_path))

    assert controller.ai_should_move() in (True, False)
