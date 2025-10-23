# Chess — Wehrmacht vs British Forces

## How to Run
1. Ensure Python 3.x is installed
2. Install required library: `pip install pygame`
3. Run the game: `python chess_1.py`

## Pre-requisites
- Python 3.x
- Pygame library
- Asset files in `assets/wehrmacht/` and `assets/british/` folders containing piece images

## How to Play
- Click on a Wehrmacht piece to select it (highlighted in green)
- Click on a highlighted destination square to move
- Legal moves are shown with green circles
- Pawn promotion: Press Q, R, B, or N when promoting
- Press SPACE to restart the game

## Screenshots
<img width="960" height="960" alt="Real Chess_ Human (Wehrmacht) vs AI (British) 10_3_2025 9_04_09 PM" src="https://github.com/user-attachments/assets/5b3277b4-3cc6-46d7-98cb-09f3974d2da5" />

## Algorithm Used
- **Minimax with Alpha-Beta Pruning**
- Depth-limited search (configurable depth)
- Piece-value based evaluation function
- Move ordering and pruning for efficiency
- Complete chess rules implementation including check, checkmate, and stalemate detection

