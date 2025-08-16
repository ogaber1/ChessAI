# ChessAI

A simple chess engine with a graphical interface built using **Python**, **Pygame**, and **python-chess**. Includes a random AI agent and an Alpha-Beta pruning AI for move selection.

## Features

* Graphical user interface (GUI) built with Pygame.
* Playable chess with legal moves enforced.
* Random AI agent.
* Alpha-Beta pruning AI for stronger play.
* Highlighting for legal moves, promotions, and check situations.

## Requirements

* Python 3.8+
* Dependencies (install via pip):

  ```bash
  pip install pygame chess
  ```

## Running from Source

1. Clone the repository:

   ```bash
   git clone https://github.com/ogaber1/ChessAI.git
   cd ChessAI
   ```

2. Run the game:

   ```bash
   python main.py
   ```

## Running the Executable

An executable version is included for convenience.

**Important:** Place the executable file **in the same directory as the `assets` folder**, otherwise the game will crash.

1. Ensure `main.exe` and the `assets/` folder are in the same directory.
2. Double-click `main.exe` to run the game.

## Controls

* **Left click**: Select and move pieces.
* **ESC**: Exit the game.

## Game Modes

* Human vs. Human
* Human vs. Random AI
* Human vs. Alpha-Beta AI

## Credits

* Built with [Pygame](https://www.pygame.org/) and [python-chess](https://python-chess.readthedocs.io/).
* Developed by [ogaber1](https://github.com/ogaber1) and [maryamyasser33](https://github.com/maryamyasser33).
