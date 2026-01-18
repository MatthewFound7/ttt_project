# testing.py
import os
import pickle
import random

# import from your module
from research.x_original_code import (
    TicTacToeEnv,
    QAgent,
    q_learning,
)  # add play_greedy_episode if you have it

MODEL_PATH = os.path.join(os.path.dirname(__file__), "imp_agent.pkl")


def load_agent(path=MODEL_PATH):
    with open(path, "rb") as f:
        Q = pickle.load(f)
    agent = QAgent()
    agent.Q = Q
    agent.epsilon = 0.0  # no exploration during testing
    return agent


def play_one_verbose_game(env, agent):
    """Plays X (agent) vs random O, printing every move."""
    s = env.reset()
    print("\nStart board:")
    env.render()
    done = False
    while not done:
        if env.current == "X":
            a = agent.greedy_action(s, env.legal_actions())
            s, r, done = env.step(a)
            print(f"\nX plays {a}")
            env.render()
        else:
            oa = random.choice(env.legal_actions())
            s, r, done = env.step(oa)
            print(f"\nO plays {oa}")
            env.render()
    print("\nResult:", "X wins" if env.winner == "X" else "O wins" if env.winner == "O" else "Draw")


if __name__ == "__main__":
    env = TicTacToeEnv()

    # 1) load if available, else train + save
    print(f"Loading agent from {MODEL_PATH} ...")
    agent = load_agent(MODEL_PATH)

    # 2) play a printed game so you see moves (not just 0..8)
    play_one_verbose_game(env, agent)

    # 3) (optional) play yourself vs the agent, if you added human_vs_agent in ttt_ai.py:
    # from ttt_ai import human_vs_agent
    # human_vs_agent(env, agent)
