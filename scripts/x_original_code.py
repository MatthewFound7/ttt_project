"""
Tic-Tac-Toe: Tabular Q-learning (epsilon-greedy)
- Agent plays X, opponent plays O (random).
- Reward from X's perspective: +1 win, -1 loss, 0 draw/otherwise.
"""

import random
from collections import defaultdict
import matplotlib.pyplot as plt

# ----- Plotting -----
x_vals, y_vals = [], []


def q_plotter(x_vals, y_vals):
    plt.plot(x_vals, y_vals, linestyle="-", label="Tic-Tac-Toe")
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward (rolling window)")
    plt.title("Tic-Tac-Toe Q-learning")
    plt.grid(True)
    plt.legend()
    plt.show()


# ----- Environment -----
class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [" "] * 9
        self.current = "X"
        self.done = False
        self.winner = None
        return self.state()

    def state(self):
        return "".join(self.board)

    def legal_actions(self):
        return [i for i, c in enumerate(self.board) if c == " "]

    def step(self, action):
        """
        Apply 'action' for the current player, return (next_state, reward_for_X, done)
        """
        # Shouldn't ever run a step if action is not on the board, or the game is finished or the action is not an empty option (SAFETY)
        if self.done or action not in range(9) or self.board[action] != " ":
            raise ValueError("Invalid action")

        # Finds the index of the action and changes it to the current move (at the start this is O the random)
        self.board[action] = self.current
        # Extracts winner player if check_winner not empty
        self.winner = self._check_winner()
        # If there is a winner, done is true, game is finished
        if self.winner or " " not in self.board:
            self.done = True

        # Reward is always from X's perspective
        reward = 0.0
        if self.done:
            if self.winner == "O":
                reward = +1.0
            elif self.winner == "X":
                reward = -1.0
            else:
                reward = 0.0

        if not self.done:
            self.current = "X" if self.current == "O" else "O"

        return self.state(), reward, self.done

    def _check_winner(self):
        b = self.board
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # cols
            (0, 4, 8),
            (2, 4, 6),  # diags
        ]
        for i, j, k in lines:
            if b[i] != " " and b[i] == b[j] == b[k]:
                return b[i]
        return None

    def render(self):
        b = self.board

        def cell(i):
            return b[i] if b[i] != " " else str(i)

        print(f"{cell(0)} | {cell(1)} | {cell(2)}")
        print("--+---+--")
        print(f"{cell(3)} | {cell(4)} | {cell(5)}")
        print("--+---+--")
        print(f"{cell(6)} | {cell(7)} | {cell(8)}")


# ----- Q-learning -----
class QAgent:
    def __init__(self, epsilon=0.0, alpha=0.0, gamma=0.0):
        self.Q = defaultdict(float)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def select_action(self, state, legal_actions):
        """
        Training-time action: with probability ε pick any legal move; otherwise pick among the argmax Q actions, breaking ties uniformly.
        """
        # epsilon-greedy over legal actions
        # First checks if there are any legal actions (game not finished)
        if not legal_actions:
            return None
        # Deciding whether we want to explore
        if random.random() < self.epsilon:
            return random.choice(legal_actions)
        # If not explore, then exploit (greedy)
        # Loops over legal actions for this string state and returns a list of the current Q-vals for each  (0 for all initially)
        qvals = [self.Q[(state, a)] for a in legal_actions]
        # Just pick the highest Q-val of the list
        maxq = max(qvals)
        # return a list of all the max vals of there are multiple that match (handles tie-breaking)
        best = [a for a, q in zip(legal_actions, qvals) if q == maxq]
        return random.choice(best)

    def greedy_action(self, state, legal_actions):
        # FOR USE IN THE "TESTING" WHEN WE WANT PURE GREEDY TO SEE PERFORMANCE
        """
        Evaluation-time action (no exploration): pure argmax with fair tie-breaking.
        """
        if not legal_actions:
            return None
        qvals = [self.Q[(state, a)] for a in legal_actions]
        maxq = max(qvals)
        best = [a for a, q in zip(legal_actions, qvals) if q == maxq]
        return random.choice(best)

    def update(self, s, a, r, s_next, legal_next, done):
        """
        Standard Q-learning update:
            If terminal (or no legal moves): target = immediate reward.
            Else: target = r + γ * max_a' Q(s_next, a').
            Incremental update toward target.
        """

        if done or not legal_next:
            target = r
        else:
            max_next = max(self.Q[(s_next, an)] for an in legal_next)
            target = r + self.gamma * max_next
        self.Q[(s, a)] += self.alpha * (target - self.Q[(s, a)])


def play_one_training_episode(env, agent, opponent="random", max_plies=9):
    """
    One full game where X (agent) and O (opponent) alternate moves.
    Returns total reward for X in the episode.
    """
    # always start each episode with a fresh game board and reward management
    s = env.reset()
    total_r = 0.0

    for _ in range(max_plies):
        if env.current == "O":
            a = agent.select_action(s, env.legal_actions())
            s_next, r, done = env.step(a)
            total_r += r

            # if game finished
            if done:
                agent.update(s, a, r, s_next, [], True)
                break

            # Opponent immediate move (random by default)
            oa = (
                random.choice(env.legal_actions())
                if opponent == "random"
                else random.choice(env.legal_actions())
            )
            s_mid, r_mid, done_mid = env.step(oa)

            if done_mid:
                agent.update(s, a, r_mid, s_mid, [], True)
                total_r += r_mid
                break
            else:
                # Non-terminal transition
                agent.update(s, a, 0.0, s_mid, env.legal_actions(), False)
                s = s_mid
        else:
            # (Shouldn't happen since X always starts, but keep robust)
            oa = random.choice(env.legal_actions())
            s, r, done = env.step(oa)
            if done:
                break

    return total_r


def q_learning(
    env,
    episodes=500,
    alpha=0.1,
    gamma=0.95,
    epsilon=0.2,
    epsilon_min=0.01,
    epsilon_decay=0.995,
    log_slices=20,
    avg_window_frac=0.2,
):
    agent = QAgent(epsilon=epsilon, alpha=alpha, gamma=gamma)
    rewards = []
    window = max(5, int(episodes * avg_window_frac))

    for ep in range(1, episodes + 1):
        # Play one training episode
        total = play_one_training_episode(env, agent, opponent="random")
        rewards.append(total)

        # Decay epsilon
        agent.epsilon = max(epsilon_min, agent.epsilon * epsilon_decay)

        # Periodic logging + plotting points
        if ep % max(1, episodes // log_slices) == 0:
            avg = sum(rewards[-window:]) / len(rewards[-window:])
            print(f"Episode {ep:5d} | eps={agent.epsilon:.3f} | avg_reward({window})={avg:.3f}")
            x_vals.append(ep)
            y_vals.append(avg)

        # if ep % 20000 == 0:  # every 500 episodes
        #     # Show the start-state values for all 9 actions
        #     chosen_state = "    O    "
        #     start_vals = {a: round(agent.Q[(chosen_state, a)], 3) for a in range(9)}
        #     print(f"Episode {ep:5d} | Q(start) = {start_vals}")

    return agent, rewards


# ----- Demo / CLI helpers -----
def play_greedy_episode(env, agent, verbose=False):
    s = env.reset()
    done = False
    steps = 0
    if verbose:
        print("\nGreedy episode (X=agent):")
        env.render()
    while not done and steps < 9:
        if env.current == "O":
            a = agent.greedy_action(s, env.legal_actions())
            s, r, done = env.step(a)
            if verbose:
                print("\nO plays", a)
                env.render()
        else:
            oa = random.choice(env.legal_actions())
            s, r, done = env.step(oa)
            if verbose:
                print("\nX plays", oa)
                env.render()
        steps += 1
    return r


def human_vs_agent(env, agent):
    """
    Human plays O and moves first.
    Agent remains X and always plays greedily.
    """
    print("\nYou are X and MOVE FIRST. Indices 0..8.")
    s = env.reset()

    # ----- Human's opening move -----
    env.render()
    legal = env.legal_actions()
    move = None
    while move not in legal:
        try:
            move = int(input(f"Your first move (choose from {legal}): "))
        except Exception:
            move = None
    s, r, done = env.step(move)
    print("\nYou played", move)
    env.render()
    if done:
        print("\nResult:", "You (X) win!" if env.winner == "X" else "Draw")
        return

    # ----- Alternating turns -----
    while True:
        a = agent.greedy_action(s, env.legal_actions())
        s, r, done = env.step(a)
        print("\nO plays", a)
        env.render()
        if done:
            print("\nResult:", "O wins!" if env.winner == "O" else "Draw")
            break

        legal = env.legal_actions()
        move = None
        while move not in legal:
            try:
                move = int(input(f"Your move (choose from {legal}): "))
            except Exception:
                move = None
        s, r, done = env.step(move)
        print("\nYou played", move)
        env.render()
        if done:
            print("\nResult:", "You (X) win!" if env.winner == "X" else "Draw")
            break


# ----- Main -----
if __name__ == "__main__":
    env = TicTacToeEnv()
    agent, rewards = q_learning(
        env,
        episodes=80000,  # 20000 for impossible to beat, 4000 for hard but easy with thought
        alpha=0.2,  # 0.2 # 0.43
        gamma=0.9,  # 0.9 # 0.92
        epsilon=0.3,  # 0.3 # 0.8
        epsilon_min=0.2,  # 0.2 # 0.005
        epsilon_decay=0.999,  # 0.999 # 0.982
    )

    # Freeze exploration for evaluation
    agent.epsilon = 0.0

    # Quick greedy run
    _ = play_greedy_episode(env, agent, verbose=True)

    # Plot rolling average reward
    q_plotter(x_vals, y_vals)

    # Uncomment to play against the trained agent:
    # human_vs_agent(env, agent)

    import pickle

    # ----- Save -----
    # with open("_agent.pkl", "wb") as f:
    #     # print(agent.Q)
    #     pickle.dump(agent.Q, f)


# import itertools
# import pickle
# import random

# # ---------- Evaluation ----------
# def evaluate_agent(env, agent, games=200, opponent='random'):
#     """
#     Play 'games' evaluation matches with agent as X (greedy policy).
#     Returns (win_rate, draw_rate, loss_rate, avg_reward).
#     """
#     wins = draws = losses = 0
#     total_reward = 0.0

#     # Freeze exploration for eval
#     old_eps = getattr(agent, "epsilon", 0.0)
#     agent.epsilon = 0.0

#     for _ in range(games):
#         s = env.reset()
#         done = False
#         # Alternate until terminal
#         while not done:
#             if env.current == 'X':
#                 # Greedy move
#                 legal = env.legal_actions()
#                 a = agent.greedy_action(s, legal)
#                 s, r, done = env.step(a)
#             else:
#                 # Opponent policy (random by default)
#                 oa = random.choice(env.legal_actions())
#                 s, r, done = env.step(oa)

#         total_reward += (1.0 if env.winner == 'X' else -1.0 if env.winner == 'O' else 0.0)
#         if env.winner == 'X':
#             wins += 1
#         elif env.winner == 'O':
#             losses += 1
#         else:
#             draws += 1

#     # restore epsilon (just in case caller expects it unchanged)
#     agent.epsilon = old_eps

#     win_rate = wins / games
#     draw_rate = draws / games
#     loss_rate = losses / games
#     avg_reward = total_reward / games
#     return win_rate, draw_rate, loss_rate, avg_reward

# # ---------- Grid Search ----------
# def grid_search(
#     param_grid,
#     episodes=3000,
#     eval_games=300,
#     repeats=2,
#     avg_window_frac=0.2,
#     seed_base=1234,
#     save_best_path="best_ttt_agent.pkl",
#     verbose=True
# ):
#     """
#     Brute-force every combo in param_grid. For each combo:
#     - Train 'repeats' times with different seeds.
#     - Score = mean win_rate over repeats (vs random O).
#     - Tracks & saves the best agent (pickle) to save_best_path.

#     param_grid: dict of hyperparameter lists, e.g.:
#         {
#           "alpha": [0.3, 0.5],
#           "gamma": [0.95, 0.99],
#           "epsilon": [0.3],
#           "epsilon_min": [0.02, 0.05],
#           "epsilon_decay": [0.999, 0.997]
#         }
#     """
#     keys = list(param_grid.keys())
#     combos = list(itertools.product(*[param_grid[k] for k in keys]))

#     best_score = -1.0
#     best_info = None   # (params_dict, score tuple, agent)
#     all_results = []   # list of dict rows for later inspection/sorting

#     for idx, values in enumerate(combos, 1):
#         params = dict(zip(keys, values))
#         rep_scores = []
#         rep_agents = []

#         for rep in range(repeats):
#             # Reproducibility per trial
#             rep_seed = seed_base + idx * 1000 + rep
#             random.seed(rep_seed)

#             # Train
#             env = TicTacToeEnv()
#             agent, _ = q_learning(
#                 env,
#                 episodes=episodes,
#                 alpha=params.get("alpha", 0.5),
#                 gamma=params.get("gamma", 0.99),
#                 epsilon=params.get("epsilon", 0.3),
#                 epsilon_min=params.get("epsilon_min", 0.02),
#                 epsilon_decay=params.get("epsilon_decay", 0.999),
#                 avg_window_frac=avg_window_frac,
#                 log_slices=10  # modest logging inside q_learning
#             )

#             # Evaluate
#             win_rate, draw_rate, loss_rate, avg_reward = evaluate_agent(env, agent, games=eval_games)
#             rep_scores.append((win_rate, draw_rate, loss_rate, avg_reward))
#             rep_agents.append(agent)

#         # Mean across repeats
#         mean_win = sum(s[0] for s in rep_scores) / repeats
#         mean_draw = sum(s[1] for s in rep_scores) / repeats
#         mean_loss = sum(s[2] for s in rep_scores) / repeats
#         mean_avg_reward = sum(s[3] for s in rep_scores) / repeats

#         # Primary objective: maximize win_rate; tie-break on avg_reward
#         score_tuple = (mean_win, mean_avg_reward)

#         # record row
#         row = {
#             **params,
#             "mean_win_rate": round(mean_win, 4),
#             "mean_draw_rate": round(mean_draw, 4),
#             "mean_loss_rate": round(mean_loss, 4),
#             "mean_avg_reward": round(mean_avg_reward, 4),
#         }
#         all_results.append(row)

#         if verbose:
#             print(f"[{idx}/{len(combos)}] params={params} "
#                   f"-> win={mean_win:.3f}, draw={mean_draw:.3f}, loss={mean_loss:.3f}, avgR={mean_avg_reward:.3f}")

#         # Update best
#         if score_tuple > (best_info[1] if best_info else (-1.0, -1.0)):
#             # Pick the rep agent with best win_rate in this combo to save
#             best_rep_ix = max(range(repeats), key=lambda i: rep_scores[i][0])
#             best_agent_for_combo = rep_agents[best_rep_ix]

#             # Persist best agent so far
#             with open(save_best_path, "wb") as f:
#                 pickle.dump(best_agent_for_combo.Q, f)

#             best_info = (params, score_tuple, best_agent_for_combo)
#             best_score = mean_win
#             if verbose:
#                 print(f"  -> NEW BEST. Saved to {save_best_path}")

#     # Sort all results by win rate then avg reward
#     all_results.sort(key=lambda r: (r["mean_win_rate"], r["mean_avg_reward"]), reverse=True)

#     return {
#         "best_params": best_info[0],
#         "best_score": {"win_rate": best_info[1][0], "avg_reward": best_info[1][1]},
#         "best_agent": best_info[2],
#         "results_table": all_results,
#         "saved_path": save_best_path
#     }

# # ---------- Loader helper for reuse ----------
# def load_agent(path="best_ttt_agent.pkl"):
#     with open(path, "rb") as f:
#         loaded_Q = pickle.load(f)
#     agent = QAgent()
#     agent.Q = loaded_Q
#     agent.epsilon = 0.0
#     return agent


# if __name__ == "__main__":
#     # 1) Define your grid
#     param_grid = {
#         "alpha": [round(x * 0.05, 2) for x in range(1, 20)],
#         "gamma": [round(x * 0.01, 2) for x in range(95, 100)],
#         "epsilon": [round(x * 0.1, 2) for x in range(1, 9)],
#         "epsilon_min": [0.02, 0.05],
#         "epsilon_decay": [0.999, 0.997, 0.995, 0.993, 0.991]
#     }

#     # 2) Run grid search (this will take some time—reduce combos or episodes if needed)
#     search_out = grid_search(
#         param_grid,
#         episodes=4000,     # training episodes per trial
#         eval_games=500,    # evaluation games per trial
#         repeats=2,         # average over 2 independent runs per combo
#         verbose=True
#     )

#     print("\nBest hyperparameters:", search_out["best_params"])
#     print("Best score:", search_out["best_score"])
#     print("Saved model path:", search_out["saved_path"])
#     # Optional: inspect top 5 rows
#     for row in search_out["results_table"][:5]:
#         print(row)

#     # 3) Load the best model later
#     best_agent = load_agent(search_out["saved_path"])
#     env = TicTacToeEnv()
#     print("\nGreedy evaluation with loaded agent:")
#     win, draw, loss, avgR = evaluate_agent(env, best_agent, games=300)
#     print(f"win={win:.3f}, draw={draw:.3f}, loss={loss:.3f}, avgR={avgR:.3f}")
