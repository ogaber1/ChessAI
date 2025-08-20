import chess
import random

def random_agent(board):
    # Select a random legal move from the board
    moves = list(board.legal_moves)
    if not moves:
        return None
    return random.choice(moves)

def alpha_beta_search(board, depth, alpha=float('-inf'), beta=float('inf'), root=True):
    if depth == 0 or board.is_game_over(): # Base case for recursion
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if not legal_moves:  # No moves — game over
        return None if root else evaluate_board(board) # Else may be Draw/Checkmate

    best_move = None
    for move in legal_moves:
        board.push(move)
        # Negate score for opponent's perspective, function is called recursively with depth - 1, and swap alpha and beta
        score = -alpha_beta_search(board, depth - 1, -beta, -alpha, root=False) 
        board.pop()

        if score > alpha: # Maximizing player wants the highest score
            alpha = score
            best_move = move

        if alpha >= beta:# Pruning Condition  
            break

    return best_move if root else alpha


def evaluate_board(board):
    # Evaluate the board position using a simple heuristic, Positional evaluation, Flip Arrays for Black
    # Positive for White, Negative for Black
    # Checkmate detection
    if board.is_checkmate():
        # If it's checkmate and it's our turn, we lost
        return -99999 if board.turn == chess.WHITE else 99999
    # Draw detection
    if (board.is_stalemate() or board.is_insufficient_material() or
        board.is_seventyfive_moves() or board.is_fivefold_repetition() or
        board.is_fifty_moves() or board.is_repetition()):
        return 0

    piece_values = {
        # Piece values based on standard chess evaluation, times 100 for easier calculations
        # Bishop is usually slightly more valued than Knight
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

    # Piece-square tables (simplified, for White; Black is mirrored)
    pawn_table = [# indexing is different than board, starting row for pawns is 2nd row here 
         0,  5,  5, -10,-10,  5,  5,  0,
         0, 10,-10,   0,  0,-10, 10,  0,
         0, 10, 10,  20, 20, 10, 10,  0,
         5, 20, 20,  30, 30, 20, 20,  5,
        10, 20, 20,  40, 40, 20, 20, 10,
        50, 50, 50,  50, 50, 50, 50, 50,
        90, 90, 90,  90, 90, 90, 90, 90,
         0,  0,  0,   0,  0,  0,  0,  0
    ]
    knight_table = [#Knights are valued more in the center of the board
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    bishop_table = [ # Bishops are generally valued more in the center of the board
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    rook_table = [ # Rooks are valued more on the 7th rank
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

    tables = { # dictionary of piece types to their respective tables
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
            table = tables[piece.piece_type]
            idx = square if piece.color == chess.WHITE else chess.square_mirror(square) # Flips the board vertically for black
            sign = 1 if piece.color == chess.WHITE else -1
            value += sign * (piece_values[piece.piece_type] + table[idx])

    # Add bonus for capturing opponent pieces
    for move in board.legal_moves:
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                value += piece_values[captured_piece.piece_type] * (1 if board.turn == chess.WHITE else -1)

    # Favor giving check: add a smaller bonus
    if board.is_check():
        value += 100 if board.turn == chess.BLACK else -100

    return value

def is_piece_safe(board, square):
    """Check if a piece on the given square is safe (not under attack)."""
    for move in board.legal_moves:
        if move.to_square == square:
            return False  # The piece is under attack
    return True
