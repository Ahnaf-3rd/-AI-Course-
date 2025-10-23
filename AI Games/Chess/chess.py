import pygame
import sys
import math
import os
import time

# --- Game Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess: Wehrmacht vs the British")

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
CHECK_RED = (255, 0, 0)
TEXT_COLOR = (40, 40, 40)

# Font for messages
MSG_FONT = pygame.font.SysFont("Arial", 40)

# --- Asset Loading ---
PIECES = {}
def load_piece_images():
    sides = ["wehrmacht", "british"]
    types = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"] 
    kind_to_file = {'Pawn': 'pawn', 'Rook': 'rook', 'Knight': 'knight', 
                    'Bishop': 'bishop', 'Queen': 'queen', 'King': 'king'}

    for side in sides:
        PIECES[side] = {}
        for kind in types:
            file_name = kind_to_file[kind]
            path = os.path.join("assets", side, f"{file_name}.png")
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
                PIECES[side][kind] = img
            except pygame.error:
                PIECES[side][kind] = None 

# Attempt to load images on startup
load_piece_images()



# --- Chess Logic Classes ---

class Piece:
    def __init__(self, side, kind):
        self.side = side 
        self.kind = kind 

class Move:
    def __init__(self, start_sq, end_sq, board, is_promotion=False):
        self.start_row, self.start_col = start_sq
        self.end_row, self.end_col = end_sq
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_promotion = is_promotion
        self.promotion_piece = Piece(self.piece_moved.side, "Queen") if is_promotion else None

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.start_row == other.start_row and self.start_col == other.start_col and \
                   self.end_row == other.end_row and self.end_col == other.end_col
        return False

class GameState:
    def __init__(self):
        self.board = self._init_board()
        self.white_to_move = True # Wehrmacht starts turn false if British
        self.wehrmacht_king_loc = (7, 4)
        self.british_king_loc = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def _init_board(self):
        board = [[None]*8 for _ in range(8)]
        # Wehrmacht (White/Human)
        for i in range(8):
            board[6][i] = Piece("wehrmacht", "Pawn")
        board[7] = [
            Piece("wehrmacht", "Rook"), Piece("wehrmacht", "Knight"), Piece("wehrmacht", "Bishop"),
            Piece("wehrmacht", "Queen"), Piece("wehrmacht", "King"), Piece("wehrmacht", "Bishop"),
            Piece("wehrmacht", "Knight"), Piece("wehrmacht", "Rook")
        ]
        # British (Black/AI)
        for i in range(8):
            board[1][i] = Piece("british", "Pawn")
        board[0] = [
            Piece("british", "Rook"), Piece("british", "Knight"), Piece("british", "Bishop"),
            Piece("british", "Queen"), Piece("british", "King"), Piece("british", "Bishop"),
            Piece("british", "Knight"), Piece("british", "Rook")
        ]
        return board

    def make_move(self, move, screen=None):
        """Executes a move but DOES NOT change self.white_to_move."""
        self.board[move.start_row][move.start_col] = None
        self.board[move.end_row][move.end_col] = move.piece_moved

        # Update King location
        if move.piece_moved.kind == 'King':
            if move.piece_moved.side == 'wehrmacht':
                self.wehrmacht_king_loc = (move.end_row, move.end_col)
            else:
                self.british_king_loc = (move.end_row, move.end_col)

        # Pawn promotion
        if move.piece_moved.kind == "Pawn":
            if (move.piece_moved.side == "wehrmacht" and move.end_row == 0) or \
               (move.piece_moved.side == "british" and move.end_row == 7):

                if screen:  # Human player -> ask choice
                    choice = ask_promotion_choice(screen, move.piece_moved.side)
                else:       # AI auto-queen
                    choice = "Queen"

                move.piece_moved.kind = choice

    def undo_move(self, move):
        """Reverts a move, crucial for Minimax."""
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured 

        # Revert King location
        if move.piece_moved.kind == 'King':
            if move.piece_moved.side == 'wehrmacht':
                self.wehrmacht_king_loc = (move.start_row, move.start_col)
            else:
                self.british_king_loc = (move.start_row, move.start_col)

        self.checkmate = False
        self.stalemate = False

    def get_valid_moves(self):
        #Returns all moves that DO NOT leave the player's own King in check.
        moves = self.get_pseudo_legal_moves()
        legal_moves = []
        current_player_side = "wehrmacht" if self.white_to_move else "british"
        
        for move in moves:
            # 1. Temporarily make the move
            self.make_move(move)
            
            # 2. Check if the current player's King is in check 
            #    We use is_square_attacked and tell it the opponent's side
            king_r, king_c = self.wehrmacht_king_loc if self.white_to_move else self.british_king_loc
            
            # The square is attacked by the opponent if the opponent's moves can reach it
            if not self.is_square_attacked(king_r, king_c, current_player_side):
                legal_moves.append(move)
                
            # 3. Undo the move (backtrack)
            self.undo_move(move)
            
        # Check for game over conditions
        if len(legal_moves) == 0:
            # We need to check if the King is currently in check (before any move attempt)
            if self.is_in_check(current_player_side):
                self.checkmate = True
            else:
                self.stalemate = True
                
        return legal_moves

    def is_in_check(self, king_side=None):
        """Checks if the specified side's King is currently under attack."""
        if king_side is None:
            king_side = "wehrmacht" if self.white_to_move else "british"

        king_loc = self.wehrmacht_king_loc if king_side == "wehrmacht" else self.british_king_loc
        return self.is_square_attacked(king_loc[0], king_loc[1], king_side)


    def is_square_attacked(self, r, c, target_side):
        """Checks if the square (r, c) is attacked by the OPPONENT of target_side."""
        
        # We need to know who the attacker is (the opponent)
        # So we temporarily set 'white_to_move' to the attacker's turn
        attacker_is_white = (target_side == "british") 
        original_white_to_move = self.white_to_move 
        
        self.white_to_move = attacker_is_white 
        
        # Generate the attacker's pseudo-legal moves
        attacker_moves = self.get_pseudo_legal_moves()
        
        # Restore the original turn state immediately after generating moves
        self.white_to_move = original_white_to_move

        for move in attacker_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False
        
    def get_pseudo_legal_moves(self):
        """Generates all possible moves for the current player, ignoring King safety."""
        moves = []
        current_side = "wehrmacht" if self.white_to_move else "british"
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece.side == current_side:
                    self._generate_piece_moves(r, c, moves)
        return moves

    # --- Piece-specific Move Generation (Standard Chess Rules) ---
    # (Remains unchanged as movement logic was already sound)
    
    def _generate_piece_moves(self, r, c, moves):
        piece = self.board[r][c]
        side = piece.side
        kind = piece.kind
        opponent_side = "british" if side == "wehrmacht" else "wehrmacht"

        if kind == "Pawn":
            dir = -1 if side == "wehrmacht" else 1
            start_row = 6 if side == "wehrmacht" else 1

            if 0 <= r + dir < 8 and not self.board[r + dir][c]:
                is_promotion = (r + dir == 0) or (r + dir == 7)
                moves.append(Move((r, c), (r + dir, c), self.board, is_promotion))
                if r == start_row and not self.board[r + 2 * dir][c]:
                    moves.append(Move((r, c), (r + 2 * dir, c), self.board))

            for dc in [-1, 1]:
                if 0 <= c + dc < 8 and 0 <= r + dir < 8:
                    target = self.board[r + dir][c + dc]
                    if target and target.side == opponent_side:
                        is_promotion = (r + dir == 0) or (r + dir == 7)
                        moves.append(Move((r, c), (r + dir, c + dc), self.board, is_promotion))

        elif kind in ["Rook", "Bishop", "Queen"]:
            directions = {
                "Rook": [(1,0),(-1,0),(0,1),(0,-1)],
                "Bishop": [(1,1),(-1,-1),(1,-1),(-1,1)],
                "Queen": [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
            }[kind]
            
            for dr, dc in directions:
                for step in range(1, 8):
                    end_r, end_c = r + dr * step, c + dc * step
                    if 0 <= end_r < 8 and 0 <= end_c < 8:
                        target = self.board[end_r][end_c]
                        if not target:
                            moves.append(Move((r, c), (end_r, end_c), self.board))
                        elif target.side == opponent_side:
                            moves.append(Move((r, c), (end_r, end_c), self.board))
                            break 
                        else: 
                            break
                    else:
                        break

        elif kind == "Knight":
            candidates = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr, dc in candidates:
                end_r, end_c = r + dr, c + dc
                if 0 <= end_r < 8 and 0 <= end_c < 8:
                    target = self.board[end_r][end_c]
                    if not target or target.side == opponent_side:
                        moves.append(Move((r, c), (end_r, end_c), self.board))

        elif kind == "King":
            candidates = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for dr, dc in candidates:
                end_r, end_c = r + dr, c + dc
                if 0 <= end_r < 8 and 0 <= end_c < 8:
                    target = self.board[end_r][end_c]
                    if not target or target.side == opponent_side:
                        moves.append(Move((r, c), (end_r, end_c), self.board))


# --- AI with Minimax (Alpha-Beta Pruning) ---

PIECE_VALUES = {"Pawn":1, "Knight":3, "Bishop":3, "Rook":5, "Queen":9, "King":1000}

def evaluate(gs):
    """Scores the board from the British (AI/Black) perspective."""
    if gs.checkmate:
        return 1000000 if gs.white_to_move else -1000000
    if gs.stalemate:
        return 0

    score = 0
    for row in gs.board:
        for piece in row:
            if piece:
                val = PIECE_VALUES.get(piece.kind, 0)
                score += val if piece.side == "british" else -val
    return score

def find_ai_move(gs, depth=7):
    """AI entry point, calls Minimax."""
    global next_move
    next_move = None
    
    # British (AI) is the maximizing player
    minimax_alpha_beta(gs, depth, -math.inf, math.inf, True)
    return next_move

def minimax_alpha_beta(gs, depth, alpha, beta, maximizing):
    """Minimax with Alpha-Beta Pruning."""
    global next_move
    
    # Base Case
    if depth == 0 or gs.checkmate or gs.stalemate:
        return evaluate(gs)

    # Temporarily switch turn to ensure get_valid_moves works for the current side
    original_white_to_move = gs.white_to_move
    gs.white_to_move = not maximizing # If maximizing (AI/British), turn must be British (False)
    
    valid_moves = gs.get_valid_moves()
    
    # Restore the turn state
    gs.white_to_move = original_white_to_move 

    import random
    random.shuffle(valid_moves)

    if maximizing: # British (AI) turn - Maximize
        max_eval = -math.inf
        for move in valid_moves:
            # 1. Make move and flip turn manually
            gs.make_move(move)
            gs.white_to_move = not gs.white_to_move 
            
            # 2. Recurse (now minimizing)
            eval = minimax_alpha_beta(gs, depth-1, alpha, beta, False)
            
            # 3. Undo move and flip turn back manually
            gs.white_to_move = not gs.white_to_move
            gs.undo_move(move)
            
            if eval > max_eval:
                max_eval = eval
                if depth == 2: 
                    next_move = move
            
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break 
        return max_eval
    else: # Wehrmacht (Human) turn - Minimize
        min_eval = math.inf
        for move in valid_moves:
            # 1. Make move and flip turn manually
            gs.make_move(move)
            gs.white_to_move = not gs.white_to_move 
            
            # 2. Recurse (now maximizing)
            eval = minimax_alpha_beta(gs, depth-1, alpha, beta, True)
            
            # 3. Undo move and flip turn back manually
            gs.white_to_move = not gs.white_to_move
            gs.undo_move(move)
            
            if eval < min_eval:
                min_eval = eval
                
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# --- Drawing ---
def draw_pieces(screen, gs):
    """Draws pieces using images or falls back to Unicode if images are missing."""
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece:
                img = PIECES.get(piece.side, {}).get(piece.kind)
                if img:
                    screen.blit(img, (c*CELL_SIZE, r*CELL_SIZE))


def draw_board(gs, selected_sq, legal_moves):
    """Draws the board, highlights, and pieces."""
    for r in range(8):
        for c in range(8):
            color = WHITE if (r+c)%2==0 else BROWN
            pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Highlight selected square
            if selected_sq == (r,c):
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(100)
                s.fill(HIGHLIGHT)
                screen.blit(s, (c*CELL_SIZE, r*CELL_SIZE))

            # Highlight King if in check
            # Check the current player's King location
            king_r, king_c = gs.wehrmacht_king_loc if gs.white_to_move else gs.british_king_loc
            if gs.is_in_check() and (r,c) == (king_r, king_c):
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(150)
                s.fill(CHECK_RED)
                screen.blit(s, (c*CELL_SIZE, r*CELL_SIZE))

            # Highlight legal moves (dot on target squares)
            for move in legal_moves:
                if move.end_row == r and move.end_col == c:
                    pygame.draw.circle(screen, HIGHLIGHT, 
                                       (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), 
                                       CELL_SIZE // 6)
    
    draw_pieces(screen, gs)

def draw_game_over_message(screen, gs):
    """Draws a game over message overlay that scales to any screen size."""
    message = ""
    if gs.stalemate:
        message = "STALEMATE (DRAW)"
    elif gs.checkmate:
        winner = "THE BRITISH" if gs.white_to_move else "WEHRMACHT"
        message = f"{winner} WINS (CHECKMATE)!"

    if message:
        width, height = screen.get_size()  # get actual screen size
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180)) 
        screen.blit(s, (0, 0))

        # Dynamic font size based on screen height
        font_size = max(24, height // 12)   # e.g. 800px screen → ~66px font
        font = pygame.font.SysFont("Arial", font_size, bold=True)

        # Main message
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2 - font_size))
        screen.blit(text, text_rect)

        # Restart hint (slightly smaller font)
        sub_font = pygame.font.SysFont("Arial", font_size // 2, bold=True)
        restart_text = sub_font.render("Press SPACE to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + font_size))
        screen.blit(restart_text, restart_rect)


# --- Add this function near the top of your file ---
def ask_promotion_choice(screen, side):
    """Show a small menu asking which piece to promote into."""
    font = pygame.font.SysFont("Arial", 32, True)
    choices = ["Queen", "Rook", "Bishop", "Knight"]
    box_width, box_height = 300, 80
    x, y = WIDTH//2 - box_width//2, HEIGHT//2 - box_height//2

    # Draw background box
    pygame.draw.rect(screen, (200,200,200), (x, y, box_width, box_height))
    pygame.draw.rect(screen, (0,0,0), (x, y, box_width, box_height), 3)

    # Render text
    text = font.render("Promote to: Q R B N", True, (0,0,0))
    screen.blit(text, (x+20, y+20))
    pygame.display.flip()

    # Wait for input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: return "Queen"
                if event.key == pygame.K_r: return "Rook"
                if event.key == pygame.K_b: return "Bishop"
                if event.key == pygame.K_n: return "Knight"


# --- Main Loop ---
def main():
    global next_move
    gs = GameState()
    running = True
    selected_sq = None
    player_clicks = []
    ai_thinking = False
    
    valid_moves = gs.get_valid_moves()
    highlight_moves = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and gs.white_to_move and not gs.checkmate and not gs.stalemate:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                
                # Human Move Logic
                if selected_sq == (row, col):
                    selected_sq = None
                    player_clicks = []
                    highlight_moves = []
                else:
                    if not selected_sq:
                        piece = gs.board[row][col]
                        if piece and piece.side == "wehrmacht":
                            selected_sq = (row, col)
                            player_clicks.append(selected_sq)
                            highlight_moves = [m for m in valid_moves if m.start_row == row and m.start_col == col]
                    elif len(player_clicks) == 1:
                        target_sq = (row, col)
                        move = Move(player_clicks[0], target_sq, gs.board)
                        
                        if move in valid_moves:
                            # Execute the move and flip the turn
                            gs.make_move(move, screen)
                            gs.white_to_move = not gs.white_to_move # Flip turn for the AI
                            
                            valid_moves = gs.get_valid_moves() 
                            selected_sq = None
                            player_clicks = []
                            highlight_moves = []
                        else:
                            # Re-select piece if invalid move
                            new_piece = gs.board[row][col]
                            if new_piece and new_piece.side == "wehrmacht":
                                selected_sq = (row, col)
                                player_clicks = [selected_sq]
                                highlight_moves = [m for m in valid_moves if m.start_row == row and m.start_col == col]
                            else:
                                selected_sq = None
                                player_clicks = []
                                highlight_moves = []
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart the game
                gs = GameState()
                selected_sq = None
                player_clicks = []
                ai_thinking = False
                valid_moves = gs.get_valid_moves()
                highlight_moves = []
        
        # AI (The British) Turn
        if not gs.white_to_move and not gs.checkmate and not gs.stalemate and not ai_thinking:
            ai_thinking = True
            
            time.sleep(0.1) 
            
            # AI (Black/British) plays
            ai_move = find_ai_move(gs, depth=2) 
            
            if ai_move:
                # Execute the move and flip the turn
                gs.make_move(ai_move)
                gs.white_to_move = not gs.white_to_move # Flip turn for the Human
                
                valid_moves = gs.get_valid_moves()
                
            ai_thinking = False

        # Drawing
        draw_board(gs, selected_sq, highlight_moves)
        draw_game_over_message(screen, gs)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
