"""
Reinforcement Learning in ~100 lines:
- A toy 1D world with 7 cells: [S, ., ., ., ., ., G]
- Start at S (index 0). Goal G (index 6) gives +1 reward and ends the episode.
- Stepping off the left edge gives -1 reward and ends the episode (a "bad" terminal).
- Actions: 0 = LEFT, 1 = RIGHT
- We learn with tabular Q-learning + epsilon-greedy exploration.
"""

import random
from collections import defaultdict
import matplotlib.pyplot as plt

x_vals = []
y_vals = []
# x_count = 0


# ----- Plotting -----
def q_plotter(x_vals, y_vals):
    plt.plot(x_vals, y_vals, linestyle="-", color="b", label="1D")

    # Add labels and title
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward")
    plt.title("1D Toy Results")
    plt.grid(True)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()


# ----- Environment -----
class OneDWorld:
    def __init__(self, n_cell=7, start=0, goal=6):
        self.n_cell = n_cell
        self.start = start
        self.goal = goal
        self.reset()

    def reset(self):
        """Ensure you always begin with position of the player at 0"""
        self.pos = self.start
        return self.pos

    def step(self, action):
        """
        Defines what happens in the environment based on an inputted action
        """
        # action: 0=left, 1=right
        if action == 0:
            next_pos = self.pos - 1
        else:
            next_pos = self.pos + 1

        # Terminal conditions
        if next_pos < 0:
            # Fell off left edge (bad terminal)
            reward, done = -1.0, True
            next_pos = 0  # snap for display; episode ends anyway
        # elif next_pos >= self.n_cell:
        #     # Stepped beyond right edge (treat as staying at last cell)
        #     next_pos = self.n_cell - 1
        #     reward, done = 0.0, False
        elif next_pos == self.goal:
            # Reached goal (good terminal)
            reward, done = +1.0, True
        else:
            reward, done = 0.0, False

        self.pos = next_pos
        return next_pos, reward, done

    def render_policy(self, Q):
        """
        Visualize the greedy policy learned at each state (ignoring terminals)
        """
        symbols = []
        for s in range(self.n_cell):
            if s == self.start:
                symbols.append("S")
            elif s == self.goal:
                symbols.append("G")
            else:
                # Choose best action at state s
                a_left = Q[(s, 0)]
                a_right = Q[(s, 1)]
                # symbols.append("←" if a_left > a_right else "→")
                if a_left > a_right:
                    symbols.append("←")
                elif a_right > a_left:
                    symbols.append("→")
                else:
                    symbols.append("•")  # or: random.choice(["←", "→"]) # "•"
        print("Policy:", " ".join(symbols))


# ----- Q-learning -----
def q_learning(
    env,
    episodes=500,
    alpha=0.1,  # learning rate
    gamma=0.95,  # discount factor
    epsilon=0.2,  # initial exploration
    epsilon_min=0.01,
    epsilon_decay=0.995,
    max_steps=50,
):
    global x_count
    # random.seed(0)
    # Q-table as a dict with default 0.0
    Q = defaultdict(float)

    # Define reward store (empty)
    rewards = []

    # Cycle through selected number of episodes (cycles)
    for ep in range(1, episodes + 1):
        state = env.reset()  # always start from 0
        total = 0.0  # tracking reward during steps? and thus is defined a default value?
        done = False  # the steps begin with no terminal active

        for t in range(max_steps):
            # Epsilon-greedy action selection
            if (
                random.random() < epsilon
            ):  # if epsilon starts high then always random action (exploration), if epsilon starts low then always picking high Q (exploitation)
                action = random.choice([0, 1])  # explore
            else:
                # exploit: pick action with higher Q
                q_left = Q[(state, 0)]
                q_right = Q[(state, 1)]
                # Important: ties are getting broken here by defining action as right (bias), but could be changed to random instead
                action = 0 if q_left > q_right else 1
                # for a more random tie break \/
                # action = random.choice([0,1]) if q_left == q_right else (0 if q_left > q_right else 1)

            # Send the selected action to the environment to decide the situation
            next_state, reward, done = env.step(action)
            total += reward

            # Q-learning update
            best_next = max(
                Q[(next_state, 0)], Q[(next_state, 1)]
            )  # best action based on probability
            Q[(state, action)] += alpha * (
                reward + gamma * best_next - Q[(state, action)]
            )  # LR x (TD ERROR) added to the current Q return

            # compute new state
            state = next_state

            # Obviously, if done then we can leave (dont have to go through all steps)
            if done:
                break

        # Add this episodes cumulative total from all the steps to the rewards list as its own individual item
        rewards.append(total)

        # Slowly reduce exploration
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        # Light progress log (EVERY X EPISODES)
        div = 20
        if ep % (episodes // div) == 0:
            # x_count += (episodes // div)
            avg = sum(rewards[-(episodes // 5) :]) / (episodes // 5)
            y_vals.append(avg)
            print(f"Episode {ep:4d} | epsilon={epsilon:.3f} | avg reward ~ {avg:.3f}")
            env.render_policy(Q)
            x_vals.append(ep)

    # After all episodes (and steps within) played through, return the rewards total for each episode, and the Q return at the end
    return Q, rewards


# ----- Demo -----
if __name__ == "__main__":
    env = OneDWorld(n_cell=7, start=0, goal=6)
    Q, rewards = q_learning(env, episodes=400)

    # Show the greedy policy after learning
    env.render_policy(Q)

    # Run one greedy episode to see behavior
    s = env.reset()
    path = [s]
    done = False
    steps = 0
    while not done and steps < 30:
        a = 0 if Q[(s, 0)] > Q[(s, 1)] else 1
        s, r, done = env.step(a)
        path.append(s)
        steps += 1

    print("Greedy path (state indices):", path)
    print("Total steps:", steps)
    q_plotter(x_vals, y_vals)
