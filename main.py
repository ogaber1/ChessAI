import chess
import pygame
from gui import draw_board, draw_pieces, get_square_under_mouse, draw_highlights, draw_promotion_highlight, draw_check_highlight, draw_message
from chess_ai import random_agent, alpha_beta_search

pygame.init()

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Agent Modes")

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
if mode == 1:
    white_agent = "human"
    black_agent = "random"
    black_depth = None
elif mode == 2:
    white_agent = "human"
    black_agent = "alpha"
    black_depth = 4
elif mode == 3:
    white_agent = "human"
    black_agent = "alpha"
    black_depth = 6
elif mode == 4:
    white_agent = "alpha"
    white_depth = 4
    black_agent = "random"
    black_depth = None
elif mode == 5:
    white_agent = "alpha"
    white_depth = 4
    black_agent = "alpha"
    black_depth = 6
else:
    white_agent = "human"
    black_agent = "random"
    black_depth = None

def check_game_over(board, screen, square_size):
    if board.is_stalemate():
        draw_message(screen, "Stalemate!", square_size)
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds
        return True
    elif board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        draw_message(screen, f"Checkmate! {winner} wins!", square_size)
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds
        return True
    return False

while running:
    if board.is_game_over():
        if check_game_over(board, screen, SQUARE_SIZE):
            running=False
            continue  # Exit the main loop immediately
    draw_board(screen, SQUARE_SIZE)
    draw_pieces(screen, board, SQUARE_SIZE)
    draw_highlights(screen, selected_square, legal_moves, SQUARE_SIZE)
    pygame.display.flip()
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Human move (White)
        elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE and white_agent == "human":
            clicked_square = get_square_under_mouse(SQUARE_SIZE)
            if selected_square is None:
                selected_square = clicked_square
                # Get legal moves for the selected piece
                legal_moves = [
                    move.to_square for move in board.legal_moves
                    if move.from_square == chess.parse_square(selected_square)
                ]
            else:
                # Prevent double-clicking the same square or invalid squares
                if selected_square == clicked_square:
                    selected_square = None
                    legal_moves = []
                    continue
                try:
                    move = chess.Move.from_uci(f"{selected_square}{clicked_square}")
                    if (board.piece_at(chess.parse_square(selected_square)).piece_type == chess.PAWN and
                        chess.square_rank(move.to_square) in [0, 7]):
                        move.promotion = chess.QUEEN  # Promote to a queen
                        print(f"Promotion move: {move}")
                        draw_promotion_highlight(screen, move.to_square, SQUARE_SIZE)  # Highlight promotion square
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        legal_moves = []
                        if check_game_over(board, screen, SQUARE_SIZE):
                            running = False
                    else:
                        print("Invalid move:", move)
                except Exception as e:
                    print("Invalid move input:", e)
                selected_square = None
                legal_moves = []  # Clear legal moves after making a move

    # White AI move
    if white_agent != "human" and board.turn == chess.WHITE and running:
        if board.is_game_over():
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False
            continue
        if white_agent == "random":
            ai_move = random_agent(board)
        elif white_agent == "alpha":
            ai_move = alpha_beta_search(board, white_depth)
        if ai_move is not None and ai_move in board.legal_moves:
            board.push(ai_move)
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False
        else:
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False

    # Black AI move
    if black_agent != "human" and board.turn == chess.BLACK and running:
        if board.is_game_over():
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False
            continue
        if black_agent == "random":
            ai_move = random_agent(board)
        elif black_agent == "alpha":
            ai_move = alpha_beta_search(board, black_depth)
        if ai_move is not None and ai_move in board.legal_moves:
            board.push(ai_move)
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False
        else:
            if check_game_over(board, screen, SQUARE_SIZE):
                running = False
pygame.quit()
