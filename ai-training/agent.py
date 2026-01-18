import random
from collections import defaultdict
from typing import Optional


class QAgent:
    def __init__(self, epsilon: float = 0.0, alpha: float = 0.0, gamma: float = 0.0):
        self.q_values = defaultdict(float)
        self.epsilon = epsilon
        self.learning_rate = alpha
        self.discount_factor = gamma

    def select_action(self, state: str, legal_actions: list[int]) -> Optional[int]:
        if not legal_actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(legal_actions)

        action_values = [self.q_values[(state, action)] for action in legal_actions]
        max_value = max(action_values)

        best_actions = [a for a, value in zip(legal_actions, action_values) if value == max_value]

        return random.choice(best_actions)

    def greedy_action(self, state: str, legal_actions: list[int]) -> Optional[int]:
        if not legal_actions:
            return None

        action_values = [self.q_values[(state, action)] for action in legal_actions]
        max_value = max(action_values)

        best_actions = [
            action for action, value in zip(legal_actions, action_values) if value == max_value
        ]

        return random.choice(best_actions)

    def update_q_values(
        self,
        state: str,
        action: int,
        reward: float,
        next_state: str,
        legal_next_actions:
        list[int], terminal: bool
        ) -> None:
        if terminal or not legal_next_actions:
            target_value = reward
        else:
            max_next_value = max(
                self.q_values[(next_state, next_action)] for next_action in legal_next_actions
            )
            target_value = reward + self.discount_factor * max_next_value

        self.q_values[(state, action)] += self.learning_rate * (
            target_value - self.q_values[(state, action)]
        )
