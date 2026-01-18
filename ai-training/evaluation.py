import random

from agent import QAgent
from environment import TicTacToeEnvironment


def play_greedy_episode(
        environment: TicTacToeEnvironment, agent: QAgent, verbose: bool = False
        ) -> float:
    state = environment.reset()
    is_done = False
    step_count = 0

    if verbose:
        print("\nGreedy episode (X=agent):")
        environment.render()

    while not is_done and step_count < 9:
        if environment.current_player == "O":
            action = agent.greedy_action(state, environment.legal_actions())
            state, reward, is_done = environment.step(action)

            if verbose:
                print("\nO plays", action)
                environment.render()

        else:
            opponent_action = random.choice(environment.legal_actions())
            state, reward, is_done = environment.step(opponent_action)

            if verbose:
                print("\nX plays", opponent_action)
                environment.render()

        step_count += 1

    return reward


def human_vs_agent(environment: TicTacToeEnvironment, agent: QAgent) -> None:
    """
    Human plays O and moves first.
    Agent remains X and always plays greedily.
    """

    print("\nYou are X and MOVE FIRST. Indices 0..8.")
    state = environment.reset()

    # ----- Human's opening move -----
    environment.render()
    legal_actions = environment.legal_actions()
    player_move = None

    while player_move not in legal_actions:
        try:
            player_move = int(input(f"Your first move (choose from {legal_actions}): "))
        except Exception:
            player_move = None

    state, reward, is_done = environment.step(player_move)
    print("\nYou played", player_move)

    environment.render()
    if is_done:
        print("\nResult:", "You (X) win!" if environment.winner == "X" else "Draw")
        return

    # ----- Alternating turns -----
    while True:
        a = agent.greedy_action(state, environment.legal_actions())
        state, reward, is_done = environment.step(a)
        print("\nO plays", a)
        environment.render()

        if is_done:
            print("\nResult:", "O wins!" if environment.winner == "O" else "Draw")
            break

        legal_actions = environment.legal_actions()
        player_move = None
        while player_move not in legal_actions:
            try:
                player_move = int(input(f"Your move (choose from {legal_actions}): "))
            except Exception:
                player_move = None

        state, reward, is_done = environment.step(player_move)
        print("\nYou played", player_move)
        environment.render()

        if is_done:
            print("\nResult:", "You (X) win!" if environment.winner == "X" else "Draw")
            break
