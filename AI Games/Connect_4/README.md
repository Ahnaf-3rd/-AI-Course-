# Connect Four — Free French Air Force vs German Luftwaffe

## How to Run
1. Ensure Python 3.x is installed
2. Install required library: `pip install pygame`
3. Run the game: `python connect.py`

## Pre-requisites
- Python 3.x
- Pygame library
- Optional asset files:
  - `assets/war_background.png`
  - `assets/axis_piece.png`
  - `assets/allies_piece.png`

## How to Play
- Click on any column to drop your Axis (red) piece
- Connect four pieces horizontally, vertically, or diagonally to win
- The AI (Allies/yellow) will automatically respond
- Press 'R' to restart the game

## Screenshots
![Game Screenshot]<img width="1050" height="900" alt="Connect Four — Free French Air Force vs German Luftwaffe 10_23_2025 9_05_27 PM" src="https://github.com/user-attachments/assets/934019d3-b0cc-4c98-85c2-19bb936e3931" />


## Algorithm Used
- **Minimax with Alpha-Beta Pruning**
- Custom evaluation function scoring different board positions
- Window-based scoring for potential winning lines
- Center column preference for better positioning
- Depth-limited search with terminal node detection
