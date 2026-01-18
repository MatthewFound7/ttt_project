import random

from agent import QAgent
from environment import TicTacToeEnvironment

x_vals, y_vals = [], []


def play_one_training_episode(
    environment: TicTacToeEnvironment,
    agent: QAgent,
    opponent: str = "random",
    max_plies: int = 9
    ) -> float:
    """
    One full game where X (agent) and O (opponent) alternate moves.
    Returns total reward for X in the episode.
    """

    state = environment.reset()
    total_reward = 0.0

    for _ in range(max_plies):
        if environment.current_player == "O":
            action = agent.select_action(state, environment.legal_actions())
            next_state, reward, is_done = environment.step(action)
            total_reward += reward

            if is_done:
                agent.update_q_values(state, action, reward, next_state, [], True)
                break

            opponent_action = (
                random.choice(environment.legal_actions())
                if opponent == "random"
                else random.choice(environment.legal_actions())
            )
            intermediate_state, intermediate_reward, opponent_done = environment.step(
                opponent_action
            )

            if opponent_done:
                agent.update_q_values(
                    state, action, intermediate_reward, intermediate_state, [], True
                    )
                total_reward += intermediate_reward
                break
            else:
                agent.update_q_values(
                    state, action, 0.0, intermediate_state, environment.legal_actions(), False
                )
                state = intermediate_state
        else:
            opponent_action = random.choice(environment.legal_actions())
            state, reward, is_done = environment.step(opponent_action)
            if is_done:
                break

    return total_reward


def run_q_learning_loop(
    environment: TicTacToeEnvironment,
    episodes: int = 500,
    alpha: int = 0.1,
    gamma: int = 0.95,
    epsilon: int = 0.2,
    epsilon_min: int = 0.01,
    epsilon_decay: int = 0.995,
    log_slices: int = 20,
    avg_window_frac: int = 0.2,
) -> tuple[QAgent, list]:
    agent = QAgent(epsilon=epsilon, alpha=alpha, gamma=gamma)
    rewards = []
    averaging_window = max(5, int(episodes * avg_window_frac))

    for episode_index in range(1, episodes + 1):
        total = play_one_training_episode(environment, agent, opponent="random")
        rewards.append(total)

        agent.epsilon = max(epsilon_min, agent.epsilon * epsilon_decay)

        if episode_index % max(1, episodes // log_slices) == 0:
            average_reward = sum(rewards[-averaging_window:]) / len(rewards[-averaging_window:])
            print(
                f"Episode {episode_index:5d} | eps={agent.epsilon:.3f} | "
                f"avg_reward({averaging_window})={average_reward:.3f}"
            )
            x_vals.append(episode_index)
            y_vals.append(average_reward)

    return agent, rewards
