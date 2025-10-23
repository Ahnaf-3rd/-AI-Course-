import pygame
import sys
import math
import random

# --- Configuration ---
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (10, 10, 10)
BG_COLOR = (30, 100, 200)  # fallback if ocean image not loaded
LINE_WIDTH = 8
BOARD_ROWS = 3
BOARD_COLS = 3
CELL_SIZE = WIDTH // BOARD_COLS
FPS = 30
# Symbols
PLAYER = "Kriegsmarine"  # "X" Human player replacement (The German Navy)
AI = "Imperial Japanese Navy"  # "O" AI replacement (The Navy of the Great Empire of Japan)  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe — Kriegsmarine vs IJN")
clock = pygame.time.Clock()

# --- Load images ---
def load_scaled(path):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))
    except:
        print(f"Warning: Could not load {path}")
        return None

# Background (ocean)
ocean_bg = None
try:
    ocean_bg = pygame.image.load("assets/ocean.png").convert()
    ocean_bg = pygame.transform.smoothscale(ocean_bg, (WIDTH, HEIGHT))
except:
    print("Warning: No ocean background found")

# German Vessels (KMS Bismarck)
german_ships = [
    load_scaled("assets/bismarck.png")
]
# Japanese Vessels (HIJMS Kirishima)
japanese_ships = [
    load_scaled("assets/kirishima.png"),
]

font = pygame.font.SysFont(None, 32)

# --- Game state ---
def empty_board():
    return [None] * 9

board = empty_board()
placed_images = [None] * 9   # parallel list to lock in chosen ship image
game_over = False
current_turn = PLAYER
winner = None

def reset_game():
    global board, placed_images, game_over, current_turn, winner
    board = empty_board()
    placed_images = [None] * 9
    game_over = False
    current_turn = PLAYER
    winner = None

# --- Draw functions ---
def draw_grid():
    if ocean_bg:
        screen.blit(ocean_bg, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Draw grid lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * 2), (WIDTH, CELL_SIZE * 2), LINE_WIDTH)

def draw_symbols(board):
    for i, cell in enumerate(board):
        if cell is None:
            continue
        row = i // 3
        col = i % 3
        x = col * CELL_SIZE
        y = row * CELL_SIZE

        # If image not yet chosen for this cell (Currently only has one image per side so this is trivial)
        if placed_images[i] is None:
            if cell == PLAYER:
                placed_images[i] = random.choice ([ship for ship in german_ships if ship])
            elif cell == AI:
                placed_images[i] = random.choice ([ship for ship in japanese_ships if ship])

        # Draw the locked-in image (Only the KMS Bismarck and HIJMS Kirishima images are available)
        img = placed_images[i]
        if img:
            screen.blit(img, (x, y))

def render_message(text):
    surf = font.render(text, True, (255, 255, 255))
    rect = surf.get_rect(center=(WIDTH//2, HEIGHT - 20))
    screen.blit(surf, rect)

# --- Logic (Horizontal, vertical and diagonal) ---
WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

def check_winner(board):
    for a,b,c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return "Draw"
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if v is None]

def evaluate(board):
    w = check_winner(board)
    if w == AI: return 10
    elif w == PLAYER: return -10
    elif w == "Draw": return 0
    return None

def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)
    if score is not None:
        return score - depth if score > 0 else score + depth, None

    moves = available_moves(board)
    best_move = None
    if is_max:
        max_eval = -math.inf
        for m in moves:
            board[m] = AI
            eval_score, _ = minimax(board, depth+1, False, alpha, beta)
            board[m] = None
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = m
            alpha = max(alpha, eval_score)
            if beta <= alpha: break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for m in moves:
            board[m] = PLAYER
            eval_score, _ = minimax(board, depth+1, True, alpha, beta)
            board[m] = None
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = m
            beta = min(beta, eval_score)
            if beta <= alpha: break
        return min_eval, best_move

def best_ai_move(board):
    if board.count(None) == 9:
        return 4
    _, move = minimax(board, 0, True, -math.inf, math.inf)
    return move if move is not None else available_moves(board)[0]

# --- Main loop ---
def main():
    global board, game_over, current_turn, winner
    reset_game()
    running = True

    """if current_turn == AI:
        ai_move = best_ai_move(board)
        if ai_move is not None:
            board[ai_move] = AI
        current_turn = PLAYER"""

    while running:
        clock.tick(FPS)
        draw_grid()
        draw_symbols(board)

        if game_over:
            msg = "Draw! Press R to restart." if winner == "Draw" else f"{winner} wins! Press R to restart."
            render_message(msg)
        else:
            render_message("Your turn (Kriegsmarine). Press R to restart.")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                if current_turn == PLAYER:
                    mx, my = event.pos
                    col, row = mx // CELL_SIZE, my // CELL_SIZE
                    idx = row*3 + col
                    if 0 <= idx < 9 and board[idx] is None:
                        board[idx] = PLAYER
                        res = check_winner(board)
                        if res: game_over, winner = True, res
                        else:
                            ai_move = best_ai_move(board)
                            if ai_move is not None:
                                board[ai_move] = AI
                            res = check_winner(board)
                            if res: game_over, winner = True, res

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
