import chess
import random

def random_agent(board):
    """Choose a random legal move."""
    moves = list(board.legal_moves)
    if not moves:
        return None
    return random.choice(moves)

def alpha_beta_search(board, depth, alpha=float('-inf'), beta=float('inf'), root=True):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if not legal_moves:  # No moves — game over
        return None if root else evaluate_board(board)

    best_move = None
    for move in legal_moves:
        board.push(move)
        score = -alpha_beta_search(board, depth - 1, -beta, -alpha, root=False)
        board.pop()

        if score > alpha:
            alpha = score
            best_move = move

        if alpha >= beta:
            break

    return best_move if root else alpha


def evaluate_board(board):
    """Evaluate the board: positive for White, negative for Black, with positional heuristics."""
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

    # Piece-square tables (simplified, for White; Black is mirrored)
    pawn_table = [
         0,  5,  5, -10,-10,  5,  5,  0,
         0, 10,-10,   0,  0,-10, 10,  0,
         0, 10, 10,  20, 20, 10, 10,  0,
         5, 20, 20,  30, 30, 20, 20,  5,
        10, 20, 20,  40, 40, 20, 20, 10,
        50, 50, 50,  50, 50, 50, 50, 50,
        90, 90, 90,  90, 90, 90, 90, 90,
         0,  0,  0,   0,  0,  0,  0,  0
    ]
    knight_table = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    bishop_table = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    rook_table = [
         0,  0,  5, 10, 10,  5,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ]
    queen_table = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    king_table = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]

    tables = {
        chess.PAWN: pawn_table,
        chess.KNIGHT: knight_table,
        chess.BISHOP: bishop_table,
        chess.ROOK: rook_table,
        chess.QUEEN: queen_table,
        chess.KING: king_table
    }

    value = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Mirror the table for black pieces
            table = tables[piece.piece_type]
            idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
            sign = 1 if piece.color == chess.WHITE else -1
            value += sign * (piece_values[piece.piece_type] + table[idx])
    return value
