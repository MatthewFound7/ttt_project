import pickle
from pathlib import Path

from environment import TicTacToeEnvironment
from evaluation import play_greedy_episode
from plotting import av_reward_plotter
from train import run_q_learning_loop, x_vals, y_vals

if __name__ == "__main__":
    environment = TicTacToeEnvironment()
    agent, rewards = run_q_learning_loop(
        environment,
        episodes=80000,
        alpha=0.2,
        gamma=0.9,
        epsilon=0.3,
        epsilon_min=0.2,
        epsilon_decay=0.999,
    )

    agent.epsilon = 0.0

    _ = play_greedy_episode(environment, agent, verbose=True)

    av_reward_plotter(x_vals, y_vals)

    save_results = input("Save Results (Y/N): ")
    if save_results == "Y":
        model_name = "another_agent"
        model_path = Path(f"ai-training/models/{model_name}.pkl")

        if model_path.exists():
            print("Name already exists, Save Aborted!")
        else:
            with open(f"{model_path}", "wb") as file:
                pickle.dump(agent.q_values, file)
            print("Saved!")
