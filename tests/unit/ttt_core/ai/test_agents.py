import pickle
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple

import pytest

from ttt_core.ai.agents import QAgent, RandomAgent
from ttt_core.domain.board import Board


@pytest.fixture
def empty_board() -> Board:
    return Board()


@pytest.fixture
def partial_board() -> Board:
    board = Board()
    board.cells = ["X", "", "O", "", "", "", "", "", ""]
    return board


@pytest.fixture
def q_table_sample() -> Dict[Tuple[str, int], float]:
    return {
        ("X O      ", 1): 0.5,
        ("X O      ", 3): 1.0,
        ("X O      ", 4): 1.0,
        ("X O      ", 5): -1.0,
    }


@pytest.fixture
def q_pickle(tmp_path: Path, q_table_sample: dict) -> Path:
    file_path = tmp_path / "q_values.pkl"
    with open(file_path, "wb") as handle:
        pickle.dump(q_table_sample, handle)
    return file_path


@pytest.fixture
def agent(q_pickle: Path) -> QAgent:
    return QAgent(q_path=str(q_pickle))


@pytest.fixture
def random_agent() -> RandomAgent:
    return RandomAgent()


def test_qagent_loads_missing_key_with_zero(agent: QAgent) -> None:
    missing_key = ("X O      ", 6)

    assert isinstance(agent.q_values_load, defaultdict)
    assert agent.q_values_load[missing_key] == 0.0


def test_board_state_representation(agent: QAgent, partial_board: Board) -> None:
    state = agent._board_state(partial_board)

    assert state == "X O      "
    assert len(state) == 9


def test_choose_best_move_with_all_zero_qvalues(
    tmp_path: Path,
    partial_board: Board,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    empty_qtable = {}
    q_file = tmp_path / "empty.pkl"

    with open(q_file, "wb") as handle:
        pickle.dump(empty_qtable, handle)

    agent = QAgent(q_path=str(q_file))

    monkeypatch.setattr(random, "choice", lambda moves: moves[0])

    move = agent.choose_best_move(partial_board)

    assert move in partial_board.legal_moves()


def test_random_agent_returns_legal_move(
    random_agent: RandomAgent,
    partial_board: Board,
) -> None:
    move = random_agent.choose_random_move(partial_board)

    assert move in partial_board.legal_moves()
