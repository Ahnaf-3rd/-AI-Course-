import pygame
import sys
import math
import random
import time

# --- Configuration ---
WIDTH, HEIGHT = 700, 600
GRID_WIDTH = 7
GRID_HEIGHT = 6
CELL_SIZE = 80
RADIUS = CELL_SIZE // 2 - 5
FPS = 60

# Colors
BLUE = (0, 0, 100)
RED = (200, 0, 0)  # Axis (Luftwaffe, German Air Force)
YELLOW = (255, 215, 0)  # Allies (Free French Air Force FAFL)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT = (100, 100, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four — Free French Air Force vs German Luftwaffe")
clock = pygame.time.Clock()

# Load background
background = None
try:
    background = pygame.image.load("assets/war_background.png").convert()
    background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
except:
    print("Warning: No background found, using solid color")

# Load piece images (if available, roundels of the Luftwaffe and FAFL)
axis_piece = None
allies_piece = None

try:
    axis_piece = pygame.image.load("assets/axis_piece.png").convert_alpha()
    axis_piece = pygame.transform.smoothscale(axis_piece, (CELL_SIZE-10, CELL_SIZE-10))
except:
    print("Warning: No axis piece image found")

try:
    allies_piece = pygame.image.load("assets/allies_piece.png").convert_alpha()
    allies_piece = pygame.transform.smoothscale(allies_piece, (CELL_SIZE-10, CELL_SIZE-10))
except:
    print("Warning: No allies piece image found")

font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 48)

# --- Game state ---
def empty_board():
    return [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

board = empty_board()
current_player = "Axis"  # Axis (Luftwaffe) goes first
game_over = False
winner = None
last_move_col = -1
last_move_row = -1

def reset_game():
    global board, current_player, game_over, winner, last_move_col, last_move_row
    board = empty_board()
    current_player = "Axis" #Change to Axis for first German turn
    game_over = False
    winner = None
    last_move_col = -1
    last_move_row = -1

def drop_piece(board, col, player):
    #Drop a piece in the specified column. Returns row where it landed, or -1 if column is full.
    for row in range(GRID_HEIGHT-1, -1, -1):
        if board[row][col] is None:
            board[row][col] = player
            return row
    return -1

def check_winner(board, player):
    #Check if the specified player has won.
    # Check horizontal
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True

    # Check vertical
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True

    # Check diagonal (positive slope)
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True

    # Check diagonal (negative slope)
    for row in range(3, GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True

    return False

def is_board_full(board):
    #Check if the board is completely filled.
    for col in range(GRID_WIDTH):
        if board[0][col] is None:
            return False
    return True

# --- AI with Minimax ---
def evaluate_window(window, player):
    #Evaluate a window of 4 consecutive cells.
    score = 0
    opponent = "Allies" if player == "Axis" else "Axis"
    
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(None) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(None) == 2:
        score += 2
        
    if window.count(opponent) == 3 and window.count(None) == 1:
        score -= 4
        
    return score

def score_position(board, player):
    """Score the entire board for the given player."""
    score = 0
    
    # Score center column
    center_array = [board[i][GRID_WIDTH//2] for i in range(GRID_HEIGHT)]
    center_count = center_array.count(player)
    score += center_count * 3
    
    # Score horizontal
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            window = [board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]]
            score += evaluate_window(window, player)
    
    # Score vertical
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH):
            window = [board[row][col], board[row+1][col], board[row+2][col], board[row+3][col]]
            score += evaluate_window(window, player)
    
    # Score diagonal (positive slope)
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH - 3):
            window = [board[row][col], board[row+1][col+1], board[row+2][col+2], board[row+3][col+3]]
            score += evaluate_window(window, player)
    
    # Score diagonal (negative slope)
    for row in range(3, GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            window = [board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]]
            score += evaluate_window(window, player)
    
    return score

def get_valid_locations(board):
    """Get all columns that are not full."""
    valid_locations = []
    for col in range(GRID_WIDTH):
        if board[0][col] is None:
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    """Check if the game is over."""
    return check_winner(board, "Axis") or check_winner(board, "Allies") or is_board_full(board)

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm with alpha-beta pruning."""
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board, "Allies"):  # AI is Allies(FAFL)
                return (None, 100000000000000)
            elif check_winner(board, "Axis"):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, "Allies"))
    
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = drop_piece(board, col, "Allies")
            new_score = minimax(board, depth-1, alpha, beta, False)[1]
            board[row][col] = None  # Undo move
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = drop_piece(board, col, "Axis")
            new_score = minimax(board, depth-1, alpha, beta, True)[1]
            board[row][col] = None  # Undo move
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def best_ai_move(board, depth=4):
    """Get the best move for the AI using minimax."""
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col

# --- Drawing functions ---
def draw_board():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLUE)

    # --- Semi-transparent grid overlay ---
    grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for col in range(GRID_WIDTH):
        for row in range(GRID_HEIGHT):
            # Semi-transparent blue rectangle
            rect = (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(grid_surface, (0, 0, 150, 120), rect)  # alpha=120

            # Black circle holes
            pygame.draw.circle(grid_surface, (0, 0, 0, 200),
                              (col * CELL_SIZE + CELL_SIZE // 2,
                               row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                              RADIUS)
    screen.blit(grid_surface, (0, 0))
    # --- End semi-transparent grid overlay ---

    # Draw pieces
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if board[row][col] == "Axis":
                if axis_piece:
                    screen.blit(axis_piece,
                               (col * CELL_SIZE + 5, row * CELL_SIZE + CELL_SIZE + 5))
                else:
                    pygame.draw.circle(screen, RED,
                                      (col * CELL_SIZE + CELL_SIZE // 2,
                                       row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                                      RADIUS)
            elif board[row][col] == "Allies":
                if allies_piece:
                    screen.blit(allies_piece,
                               (col * CELL_SIZE + 5, row * CELL_SIZE + CELL_SIZE + 5))
                else:
                    pygame.draw.circle(screen, YELLOW,
                                      (col * CELL_SIZE + CELL_SIZE // 2,
                                       row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                                      RADIUS)

    # Highlight last move
    if last_move_col != -1 and last_move_row != -1:
        pygame.draw.circle(screen, HIGHLIGHT,
                          (last_move_col * CELL_SIZE + CELL_SIZE // 2,
                           last_move_row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2),
                          RADIUS // 2, 3)

def draw_ui():
    # Draw title
    title = title_font.render("CONNECT FOUR", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    
    # Draw player indicators
    axis_text = font.render("AXIS", True, RED if current_player == "Axis" else WHITE)
    allies_text = font.render("ALLIES", True, YELLOW if current_player == "Allies" else WHITE)
    
    screen.blit(axis_text, (50, 20))
    screen.blit(allies_text, (WIDTH - 100, 20))
    
    # Draw game status
    if game_over:
        if winner == "Draw":
            status = font.render("DRAW! Press R to restart", True, WHITE)
        else:
            status = font.render(f"{winner} WINS! Press R to restart", True, WHITE)
        screen.blit(status, (WIDTH // 2 - status.get_width() // 2, HEIGHT - 40))
    else:
        status = font.render(f"{current_player}'s Turn", True, WHITE)
        screen.blit(status, (WIDTH // 2 - status.get_width() // 2, HEIGHT - 40))

# --- Main loop ---
def main():
    global board, current_player, game_over, winner, last_move_col, last_move_row
    
    reset_game()
    running = True
    ai_thinking = False
    """if current_player == 'Allies': #Extra necessity for first Free French turn
        ai_thinking = True"""
    
    while running:
        clock.tick(FPS)
        
        # Draw everything
        draw_board()
        draw_ui()
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    ai_thinking = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not ai_thinking:
                if current_player == "Axis":  # Human player's turn
                    x, y = event.pos
                    col = x // CELL_SIZE
                    
                    if 0 <= col < GRID_WIDTH:
                        row = drop_piece(board, col, "Axis")
                        if row != -1:  # Valid move
                            last_move_col, last_move_row = col, row
                            
                            # Check for win or draw
                            if check_winner(board, "Axis"):
                                game_over = True
                                winner = "Axis"
                            elif is_board_full(board):
                                game_over = True
                                winner = "Draw"
                            else:
                                current_player = "Allies"  # Switch to AI
                                ai_thinking = True
        
        # AI's turn
        if current_player == "Allies" and not game_over and ai_thinking:
            # Add a small delay to make AI moves visible
            time.sleep(0.5)
            
            col = best_ai_move(board)
            if col is not None:
                row = drop_piece(board, col, "Allies")
                if row != -1:  # Valid move
                    last_move_col, last_move_row = col, row
                    
                    # Check for win or draw
                    if check_winner(board, "Allies"):
                        game_over = True
                        winner = "Allies"
                    elif is_board_full(board):
                        game_over = True
                        winner = "Draw"
                    else:
                        current_player = "Axis"  # Switch to human
            
            ai_thinking = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
