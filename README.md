# Tic-Tac-Toe: Human vs AI

A modern implementation of the classic Tic-Tac-Toe game using a Q-learning trained AI player.

## Contents
1. Introduction
2. Skills Showcased
3. Project Overview
4. Package Structure
5. Conclusion
6. About this portfolio
7. Installed Packages/Languages

Ideas to add: Key Features, Demo/screenshots, project structure, how the RL works, installation, how to run, configuration, testing, future improvements, skills showcased, tech used

Tasks
- PR process github

## 1. Introduction

Tic-Tac-Toe v3 is the current up-to-date version of one of my portfolio projects designed to demonstrate proficiency in building interactive applications with python. The project features a user-friendly UI, and showcases a variety of programming and design skills. This version includes a second page for potential statistics expansion.

## 2. Skills Showcased

- Frontend development (CustomTkinter)
- State management
- Responsive UI design
- Component-based architecture
- Routing and navigation
- Game logic implementation
- Modular code structure

## 3. Project Overview

![TicTacToeInterface](/images/TicTacToeInterface.png)

![TicTacToeInterface](/images/winner.png)

At this stage the project activities take place mainly on the interface shown above. I have broken this into 3 main sections:

1. **The Title Board (TOP)**: Title and Button directing to stats page.
2. **The Game Board (BOTTOM-LEFT)**: Grid for places pieces
3. **The Logic Manager (RIGHT)**: Displays who plays next, displays game result, and reveals play again pane.
4. **The Selection Pane (BOTTOM-RIGHT)**: Four main gamemodes. Multiplayer allows you to play against a friend. Easy mode is built by setting the user against the computer making random guesses. The harder modes are controlled by an AI trained as an agent in an environment (trial and error learning).

## 4. Package Structure
- **app**
    - **ui**
        - **assets**: contains images for the circles, crosses and arrows for directing user
        - window.py: all front-end design
    - backend.py: foundational methods designing the game logic
    - constants.py: all the data stores including tracking, UI colours etc
    - game_modes.py: building on the base backend to add and re-define methods for the computer to be able to control game logic
    - main.py: runs the package
- **models**
    - hard_agent.pkl: info on parameters and results to come...
    - imp_agent.pkl: info on paramter and results to come...
- **scripts**: details about Q-learning methodology to come...
    - agent.py: defines the abilities of the agent
    - env.py: defines the environment the agent interacts with
    - eval.py: runs through one episode of training
    - plotting.py: plot to track rewards over time
    - train.py: training methodology
- **tests**

## 5. Conclusion

Tic-Tac-Toe v3 builds on my working project in Python by adding to the interface, AI, and modular code with the potential for a statistics page!

## 6. About this Portfolio

This project is part of my personal portfolio of programming projects showcasing skills in Python.

## 7. Installed Packages/Languages

- Packages: None
- Languages: Python

### Extra Notes
- Run whole package through terminal using command: `python -m ttt_ui.main`
- The tests folder is a working progress...