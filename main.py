import chess
import pygame
from gui import draw_board, draw_pieces, get_square_under_mouse, draw_highlights, draw_promotion_highlight, draw_check_highlight, draw_message
from chess_ai import random_agent

pygame.init()

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Random Agent")

board = chess.Board()
selected_square = None
legal_moves = []
running = True
clock = pygame.time.Clock()

while running:
    draw_board(screen, SQUARE_SIZE)
    draw_pieces(screen, board, SQUARE_SIZE)
    draw_highlights(screen, selected_square, legal_moves, SQUARE_SIZE)
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Human move (White)
        elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
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
                    else:
                        print("Invalid move:", move)
                except Exception as e:
                    print("Invalid move input:", e)
                selected_square = None
                legal_moves = []  # Clear legal moves after making a move

    # Random AI move (Black)
    if not board.turn and not board.is_game_over():
        ai_move = random_agent(board)
        board.push(ai_move)

    # Check and Checkmate handling
    if board.is_stalemate():
        draw_message(screen, "Stalemate!", SQUARE_SIZE)
        pygame.display.flip()
        pygame.time.wait(60000)  # Wait for 3 seconds before quitting
        running = False
    elif board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"  # Determine the winner
        draw_message(screen, f"Checkmate! {winner} wins!", SQUARE_SIZE)
        pygame.display.flip()
        pygame.time.wait(60000)  # Wait for 3 seconds before quitting
        running = False
    elif board.is_check():
        print("Check!")
        draw_check_highlight(screen, board.king(board.turn), SQUARE_SIZE)  # Highlight the checked king

pygame.quit()
