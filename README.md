# Connect 4 — AI Bot

A Python implementation of the classic Connect 4 game featuring a graphical interface powered by Pygame and an AI 
opponent using the Minimax algorithm with alpha-beta pruning.

## Features

- Fully playable Connect 4 with GUI
- Intelligent AI opponent that’s hard to beat
- Visual feedback for game status and outcomes
- Option to replay after each game

## AI Details

The AI uses the Minimax algorithm with alpha-beta pruning and a board evaluation heuristic to choose optimal moves. The search depth is configurable and currently set to 5 for performance.

---

## File Structure

- `gui.py`: Handles all graphical rendering and game loop logic using Pygame.
- `ai.py`: Contains the AI logic including Minimax, evaluation, and move selection.
- `constants.py`: Stores game configuration values such as board size, colors, and piece types.
- `connect4.py`: **(Required)** Game logic class.

---

## Getting Started

### 1. Install Requirements

```bash
pip install pygame
```

### 2. Run the Game

```bash
python gui.py
```

---

## Dependencies

- Python 3.x
- `pygame`

---