import pytest

import ttt_ui.controllers.game_controller as controller


class FakeStats:
    def __init__(self) -> None:
        self.player_wins = 2
        self.total_games = 4

    def percent_wins(self) -> float:
        return 50.0


class FakeEngine:
    def __init__(self, stats: FakeStats) -> None:
        self._stats = stats
        self._current_mark = "X"
        self._lock = False
        self.expose_board = "X O  O   "

    def reset_game(self) -> None:
        self._current_mark = "X"

    def current_mark(self) -> str:
        return self._current_mark

    def lock_selection(self) -> bool:
        return self._lock

    def index_move_and_update_status(self, index: int) -> dict:
        return {
            "placed_index": index,
            "attempts": 1,
            "game_over": False,
            "winner": None,
            "win_line": None,
        }


class FakeAgent:
    def choose_move(self, board: object) -> int:
        return 4


@pytest.fixture
def mock_cells(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        controller,
        "CELLS",
        [
            (0.0, 0.0),
            (1.0, 0.0),
            (2.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0),
            (2.0, 1.0),
            (0.0, 2.0),
            (1.0, 2.0),
            (2.0, 2.0),
        ],
    )


@pytest.fixture
def game_controller(monkeypatch: pytest.MonkeyPatch) -> controller.GameController:
    monkeypatch.setattr(controller, "Stats", FakeStats)
    monkeypatch.setattr(controller, "Engine", FakeEngine)
    monkeypatch.setattr(controller, "RandomAgent", FakeAgent)
    monkeypatch.setattr(controller, "QAgent", lambda path: FakeAgent())

    return controller.GameController()


def test_coord_to_index_finds_nearest_cell(mock_cells: None) -> None:
    index = controller.coord_to_index(1.1, 1.1)
    assert index == 4


@pytest.mark.parametrize(
    "mode_func, expected_agent",
    [
        ("set_mode_multi", None),
        ("set_mode_easy", "agent"),
        ("set_challenge_mode", "agent"),
    ],
)
def test_mode_selection_assigns_agent_correctly(
    game_controller: controller.GameController,
    mode_func: str,
    expected_agent: str | None,
) -> None:
    if mode_func == "set_challenge_mode":
        getattr(game_controller, mode_func)("model.pkl")
    else:
        getattr(game_controller, mode_func)()

    if expected_agent is None:
        assert game_controller._agent is None
    else:
        assert game_controller._agent is not None


def test_current_shape_returns_engine_mark(game_controller: controller.GameController) -> None:
    assert game_controller.current_shape() == "X"


def test_register_click_and_move_returns_move_result(
    game_controller: controller.GameController,
) -> None:
    result = game_controller.register_click_and_move(0.0, 0.0)

    assert result.placed_index == 0
    assert result.attempts == 1
    assert result.game_over is False
    assert result.winner == ""
    assert result.win_line is None


def test_register_ai_click_and_move_returns_move_result(
    game_controller: controller.GameController,
) -> None:
    result = game_controller.register_ai_click_and_move()

    assert result.placed_index == 4
    assert result.attempts == 1


def test_ai_should_move_false_when_x_turn(
    game_controller: controller.GameController,
) -> None:
    game_controller._engine._current_mark = "X"
    assert game_controller.ai_should_move() is False


def test_lock_selection_returns_engine_value(
    game_controller: controller.GameController,
) -> None:
    game_controller._engine._lock = True
    assert game_controller.lock_selection() is True


def test_hold_stats_returns_expected_tuple(
    game_controller: controller.GameController,
) -> None:
    wins, games, percent = game_controller.hold_stats()

    assert wins == 2
    assert games == 4
    assert percent == 50.0
