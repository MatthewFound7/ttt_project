# Tic-Tac-Toe: Human vs AI

A modern implementation of the classic Tic-Tac-Toe game using a Q-learning trained AI player.

## Contents
1. About
2. Overview
3. Reinforcement Learning (Q-learning) Integration
4. Q-Agent Configuration
5. Installation
6. Development 
7. Future & On-going Work
8. Notes on Structure

## 1. About

This game represents my first attempt at building a solid python full-stack project. I decided to keep things simple with a basic game (Tic-Tac-Toe) which has given me the opportunity to integrate something that is far more complex and which I am deeply passionate about: AI-trained models. Q-learning allows reinforcement training in python without the need of complex dependencies, which has really helped build my core python skills in OOP and separation of concerns. In this page, I cover some of my learnings, showcase the project and provide information on how to install/develop/contribute.

Skills Developed: Python (OOP, Data Structures, modular design), AI (RL, Model Evaluation), UI Development (CustomTkinter, View Control)

## 2. Overview

![TicTacToeInterface](/images/TicTacToeInterface.png)

![TicTacToeInterface](/images/winner.png)

The project activities take place mainly on the interface shown above. I have broken this into 3 main sections:

1. **The Title Board (TOP)**: Title and Button directing to stats page.
2. **The Game Board (BOTTOM-LEFT)**: Grid for placing pieces
3. **The Logic Manager (RIGHT)**: Displays who plays next, displays game result, and reveals play again pane.
4. **The Selection Pane (BOTTOM-RIGHT)**: Four main gamemodes. Multiplayer allows you to play against a friend. Easy mode is built by setting the user against the computer making random guesses. The harder modes are controlled by an AI trained as an agent in an environment (reinforcement learning with a Q-Agent).

## 3. Reinforcement Learning (Q-learning) Integration
Reinforcement Learning (RL) was always a good option for a project like this. RL is a way to train an “agent” to make decisions by **trying actions**, **receiving feedback**, and **improving over time**. Instead of being told the correct move, the agent learns from experience by maximizing a numeric reward signal. This idea of constructing an environment lends itself well to Tic-Tac-Toe because the environment is known, and the Agent does not have many move types. If this was an action game, the maths would scale really quickly due to all the factors needed to be controlled.

In this project, the RL agent plays many games (against an opponent randomly guessing). After each move, it observes the **state** (the board position) which is tracked using a `str` type, chooses an **action** (from open character spaces in the `str`), receives a **reward** (e.g., `+1` win, `0` draw, `-1` loss), and transitions to a **next state**.

The theory behind Q-learning can seem daunting but it follows some basic principles. The agent basically is tasked with learning a table of values called **Q-values**:

* **$Q(s, a)$** = “How good is it to take action `a` in state `s`?”

All these state-action pairs are stored in a massive `dict`. It updates Q-values using the Bellman update rule:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha \Big[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\Big]
$$

Where:

* $\alpha$ is the learning rate (how quickly we update beliefs),
* $\gamma$ is the discount factor (how much we value future rewards),
* $r$ is the immediate reward,
* $s'$ is the next state.

To balance exploration vs exploitation, the agent often uses **ε-greedy** selection:

$$
a =
\begin{cases}
\text{random action} & \text{with probability } \varepsilon \\
\arg\max_{a} Q(s,a) & \text{with probability } 1-\varepsilon
\end{cases}
$$

Exploration is often prioritised initially, allowing the model to explore unqiue possibilities for exploitation proceeds, to affirm confident choices.

After training, the agent uses the learned Q-table to choose strong moves, hoepfully acting as a challenging AI opponent. 

## 4. Q-Agent Configuration
The quality and perhaps difficulty, of the AI opponent is determined by the quality of the training, and this is determined by the configuration of the model, and its parameters.

The parameters used to train the agents for the game are shown below. The only difference between the two difficulties is shown in brackets:

| Parameter | Hard Difficulty Value |
| ----------- | ----------- |
| Episodes | 4'000 (20'000 for Impossible) |
| $\alpha$ | 0.2 |
| $\gamma$ | 0.9 |
| $\epsilon$ | 0.3 |
| $\epsilon_{min}$ | 0.2 |
| $\epsilon_{decay}$ | 0.999 |

Selecting the right parameters involved a lot of trial and error and there are known (and yet unexplored) methods of making this a more efficient process. The slightly basic approach taken here was to massively bump up the episodes (training games) to make a more difficult opponent. A low learning rate was needed to ensure the model didn't start over-confident and exploration is high in this model, favouring the notion that there are a relatively small number of move combinations, adn so learning all of these is more appropriate.

## 5. Installation
Clone:
``` 
git clone https://github.com/MatthewFound7/tic-tac-toe-ai.git 
```
Set-up Virtual Environment:
```
python -m venv .venv
.venv/Scripts/activate.bat
```
Download Dependencies:
```
pip install -r requirements.txt
```
Run:
```
python -m ttt_ui.main
```

## 6. Development
Download Dependencies:
```
pip install -r dev-requirements.txt
```

## 7. Future & On-going Work
- Need to add a PR process
- Need to add tests
- API integration

## 8. Notes on Structure
- Separation of concerns by creating uni-directional code flow: Training -> Backend -> Frontend
- Backend (ttt_core): 
    - AI collects training results and converts to actual game states
    - Domain handles game logic and rules
    - Engine is driver for game process
- Frontend (ttt_ui):
    - Controllers acts as bridge between UI and Game Engine
    - Services are all assets e.g. images, constants, positions, coords
    - Views structures each section of the UI
    - app.py builds all components for UI
    - main.py is where game is run from
