# Tic-Tac-Toe — Kriegsmarine vs Imperial Japanese Navy

## How to Run
1. Ensure Python 3.x is installed
2. Install required library: `pip install pygame`
3. Run the game: `python tic_tac_toe-1.py`

## Pre-requisites
- Python 3.x
- Pygame library
- Asset files (optional):
  - `assets/ocean.png` (background)
  - `assets/bismarck.png` (German ship)
  - `assets/kirishima.png` (Japanese ship)

## How to Play
- Click on any empty grid cell to place your Kriegsmarine ship
- The AI (Imperial Japanese Navy) will automatically respond
- Get three of your ships in a row (horizontally, vertically, or diagonally) to win
- Press 'R' to restart the game at any time

## Screenshots
<img width="900" height="900" alt="Tic-Tac-Toe — Kriegsmarine vs IJN 10_23_2025 8_58_11 PM" src="https://github.com/user-attachments/assets/f9863049-f86a-494c-9f28-9f51c4caf891" />

## Algorithm Used
- **Minimax with Alpha-Beta Pruning**
- The AI evaluates all possible moves to determine the optimal strategy
- Implements depth-limited search with heuristic evaluation
