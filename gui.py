import pygame
import chess
import os

IMAGES = {}

def load_images(square_size):
    pieces = ['wp', 'wn', 'wb', 'wr', 'wq', 'wk',
              'bp', 'bn', 'bb', 'br', 'bq', 'bk']
    for piece in pieces:
        path = os.path.join("assets", f"{piece}.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing image: {path}")
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(path), (square_size, square_size)
        )

def draw_board(screen, square_size):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, (c*square_size, r*square_size, square_size, square_size))

def draw_pieces(screen, board, square_size):
    if not IMAGES:
        load_images(square_size)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            color_prefix = 'w' if piece.color == chess.WHITE else 'b'
            img_key = color_prefix + piece.symbol().lower()
            screen.blit(IMAGES[img_key], (col*square_size, row*square_size))

def get_square_under_mouse(square_size):
    mx, my = pygame.mouse.get_pos()
    col = mx // square_size
    row = my // square_size
    return f"{chr(col + ord('a'))}{7 - row + 1}"

if __name__ == "__main__":
    pygame.init()
    WIDTH = HEIGHT = 640
    SQUARE_SIZE = WIDTH // 8
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    board = chess.Board()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_board(screen, SQUARE_SIZE)
        draw_pieces(screen, board, SQUARE_SIZE)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
