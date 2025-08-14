import chess
import random

def random_agent(board):
    """Choose a random legal move."""
    return random.choice(list(board.legal_moves))
