# from src.game import Game
# from src.board import Board
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square
from src.functions.find_moves import find_available_moves
from src.functions.squares_controlled import (
    ControlledSquares, 
    find_squares_controlled
)
import logging
logger = logging.getLogger(__name__)

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
    sq_black = space_control(board, 'black')
    sq_white = space_control(board, 'white')
    opp_sq_balance = 0
    for sq in sq_white.squares:
        opp_sq_balance += sq_white.squares[sq] 
    for sq in sq_black.squares:
        opp_sq_balance -= sq_black.squares[sq]
    eval += 0.5 * opp_sq_balance
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
    pieces = board.white() if side == "white" else board.black()
    all_squares = ControlledSquares() # convert to controlled squares obj
    opponent_squares = ControlledSquares() # convert to controlled squares obj

    for piece in pieces:
        # look forward for each piece, and see all available moves
        # if a square is on opponent's side of board, add to set
        all_squares += find_squares_controlled(board, piece)
    
    for sq in all_squares.squares:
        # logger.debug(sq)
        _, rank = parse_square(sq)
        if rank > 4 and side == 'white':
            opponent_squares.squares[sq] = all_squares.squares[sq]
        elif rank < 5 and side == 'black':
            opponent_squares.add(sq)
        
    return opponent_squares
