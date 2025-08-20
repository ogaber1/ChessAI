import chess
import pygame
from gui import draw_board, draw_pieces, get_square_under_mouse, draw_highlights, draw_promotion_highlight, draw_check_highlight, draw_message
from chess_ai import random_agent, alpha_beta_search
import time

pygame.init()

# Constants for the game
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Agent Modes")

# Function to display the mode selection screen
def mode_selection_screen(screen, square_size):
    pygame.font.init()
    font = pygame.font.Font(None, 34)
    options = [
        "1. Human vs Random Agent",
        "2. Human vs Alpha-Beta Agent (easy)",
        "3. Human vs Alpha-Beta Agent (hard)",
        "4. Alpha-Beta Agent vs Random Agent",
        "5. Alpha-Beta Agent (easy) vs Alpha-Beta Agent (hard)"
    ]
    while True:
        screen.fill((200, 200, 200))
        for i, option in enumerate(options):
            text = font.render(option, True, (0, 0, 0))
            rect = text.get_rect(center=(screen.get_width() // 2, 100 + i * 60))
            screen.blit(text, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(len(options)):
                    if 100 + i * 60 - 20 < my < 100 + i * 60 + 20:
                        return i + 1
                    

board = chess.Board()
selected_square = None
legal_moves = []
running = True
clock = pygame.time.Clock()

mode = mode_selection_screen(screen, SQUARE_SIZE)

# Set up agents and depths based on mode
if mode == 1:  # Human vs Random Agent
    white_agent = "human"
    black_agent = "random"
    black_depth = None
elif mode == 2: # Human vs Alpha-Beta Agent (easy)
    white_agent = "human"
    black_agent = "alpha"
    black_depth = 3
elif mode == 3: # Human vs Alpha-Beta Agent (hard)
    white_agent = "human"
    black_agent = "alpha"
    black_depth = 4
elif mode == 4: # Alpha-Beta Agent vs Random Agent
    white_agent = "alpha"
    white_depth = 3
    black_agent = "random"
    black_depth = None
elif mode == 5: # Alpha-Beta Agent (easy) vs Alpha-Beta Agent (hard)
    white_agent = "alpha"
    white_depth = 3
    black_agent = "alpha"
    black_depth = 4
else: # Invalid mode, default to Human vs Random Agent
    white_agent = "human"
    black_agent = "random"
    black_depth = None

# Initialize move counters and timer
white_moves = 0
black_moves = 0
start_time = time.time() 

# Function to check game over conditions and display messages
def check_game_over(board, screen, square_size):
    font = pygame.font.Font(None, 34)
    moves_msg = f"White moves: {white_moves}   Black moves: {black_moves}"
    white_material, black_material = get_material_count(board)
    material_msg = f"White material: {white_material}   Black material: {black_material}"
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        message = f"Checkmate! {winner} wins!\n{moves_msg}\n{material_msg}"
    elif board.is_stalemate():
        message = f"Stalemate!\n{moves_msg}\n{material_msg}"
    elif (board.is_fivefold_repetition() or board.is_seventyfive_moves() or
          board.is_insufficient_material() or board.is_fifty_moves() or board.is_repetition()):
        message = f"Draw!\n{moves_msg}\n{material_msg}"
    else:
        return False

    # Draw the message (multi-line support)
    screen.fill((200, 200, 200))
    for i, line in enumerate(message.split('\n')):
        text = font.render(line, True, (0, 0, 0))
        rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
        screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(10000)
    return True

# Function to get the material count for both players
def get_material_count(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    white_material = 0
    black_material = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += value
            else:
                black_material += value
    return white_material, black_material

# Main game loop
while running:
    # Draw the board and pieces
    draw_board(screen, SQUARE_SIZE)
    draw_pieces(screen, board, SQUARE_SIZE)
    draw_highlights(screen, selected_square, legal_moves, SQUARE_SIZE)

    # Timer
    elapsed = int(time.time() - start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    timer_text = f"Time: {minutes:02}:{seconds:02}"
    font = pygame.font.Font(None, 28)
    timer_surface = font.render(timer_text, True, (0, 0, 0))
    screen.blit(timer_surface, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(30)

    # Event handling, divided by agent type; Human or AI
    for event in pygame.event.get():
        # Handle quit event
        if event.type == pygame.QUIT:
            running = False

        # Human move (White)
        elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE and white_agent == "human":
            clicked_square = get_square_under_mouse(SQUARE_SIZE)
            if selected_square is None: #No piece selected
                # Clicked square is stored in selected_square and legal moves are calculated and added to legal_moves
                selected_square = clicked_square
                legal_moves = [
                    move.to_square for move in board.legal_moves
                    if move.from_square == chess.parse_square(selected_square)
                ]
            else:
                # double click on the same square deselects the piece instead of quitting
                if selected_square == clicked_square:
                    selected_square = None
                    legal_moves = []
                    continue
                try:
                    move = chess.Move.from_uci(f"{selected_square}{clicked_square}")
                    if (board.piece_at(chess.parse_square(selected_square)).piece_type == chess.PAWN and
                        chess.square_rank(move.to_square) in [0, 7]): # Promotion condition
                        # If pawn reaches the last rank, promote it to a queen(auto promotion)
                        move.promotion = chess.QUEEN
                        draw_promotion_highlight(screen, move.to_square, SQUARE_SIZE)
                    if move in board.legal_moves:# Normal move
                        # Push the move to the board and update the game state
                        board.push(move)
                        white_moves += 1
                        selected_square = None
                        legal_moves = []
                        if check_game_over(board, screen, SQUARE_SIZE):
                            running = False
                    else:
                        print("Invalid move:", move) # Invalid move 
                except Exception as e:
                    print("Invalid move input:", e) # Invalid move input (empty square to move))
                selected_square = None
                legal_moves = []

    # AI moves (White)
    if white_agent != "human" and board.turn == chess.WHITE and running:
        if check_game_over(board, screen, SQUARE_SIZE):
            running = False
            continue

        # Determine AI move based on agent type
        if white_agent == "random":
            ai_move = random_agent(board)
        elif white_agent == "alpha":
            ai_move = alpha_beta_search(board, white_depth)

        # If a valid move is found, push it to the boar
        if ai_move is not None and ai_move in board.legal_moves:
            board.push(ai_move)
            white_moves += 1
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False

    # AI moves (Black)
    if black_agent != "human" and board.turn == chess.BLACK and running:
        if check_game_over(board, screen, SQUARE_SIZE):
            running = False
            continue
        if black_agent == "random":
            ai_move = random_agent(board)
        elif black_agent == "alpha":
            ai_move = alpha_beta_search(board, black_depth)
        if ai_move is not None and ai_move in board.legal_moves:
            board.push(ai_move)
            black_moves += 1
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False

pygame.quit()
