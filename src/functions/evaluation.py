# from src.game import Game
# from src.board import Board
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

def get_evaluation(board):
    w_pieces = board.white()
    b_pieces = board.black()
    eval = count_material(w_pieces, b_pieces)
    return eval

def count_material(w_pieces, b_pieces):
    w_material, b_material = 0,0

    for piece in w_pieces:
        if type(piece) is not King:
            w_material += piece._value
            
    for piece in b_pieces:
        if type(piece) is not King:
            b_material += piece._value

    return w_material - b_material
     
def calc_king_safety(board, side):
    # For each square around the king, how many times is each attacked
    # by enemy side minus how many times is the square defended?
    # If squaes attacked, how many squares are free for the king to move into?
    # From those free squares, how many more squares are free in the path?
    pass

def piece_activity(board, piece):
    # What can this piece do if it could make multiple moves?
    # Check 1,2,3,4,5 moves, piece that can be captured is value/10 points
    # Each multi move calculated as capture._value/(10*moves)
    # Return array
    pass

def pawn_structure(board, side):
    # How many gaps are in the pawn structure?
    # Do the pawns defend eachother?
    # Are the pawns defended by other pieces?
    # Are pawns stacked?
    pass

def space_control(board, side):
    # How many squares on the other side of the board
    #   can you attack? 
    # Include squares occupied, empty squares, and 
    #   enemy pieces attacked
    pass