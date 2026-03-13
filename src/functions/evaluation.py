from src.game import Game
from src.board import Board
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square

# Order of evaluating chess position, according to Gotham:
#   1. Material count
#   2. King Safety
#   3. Piece activity/future prospects of pieces
#   4. Pawn structure
#   5. Space controlled

def count_material(game):
    w_pieces = game.board.white()
    b_pieces = game.board.black()
    w_material, b_material = 0,0

    for piece in w_pieces:
        if piece is King:
            continue
        w_material += piece._value

    for piece in b_pieces:
        if piece is King:
            continue
        b_material += piece._value

    return w_material - b_material
     