import chess
import pygame
from gui import draw_board, draw_pieces, get_square_under_mouse
from chess_ai import random_agent

pygame.init()

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Random Agent")

board = chess.Board()
selected_square = None
running = True
clock = pygame.time.Clock()

while running:
    draw_board(screen, SQUARE_SIZE)
    draw_pieces(screen, board, SQUARE_SIZE)
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
            else:
                move = chess.Move.from_uci(f"{selected_square}{clicked_square}")
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

    # Random AI move (Black)
    if not board.turn and not board.is_game_over():
        ai_move = random_agent(board)
        board.push(ai_move)

pygame.quit()
