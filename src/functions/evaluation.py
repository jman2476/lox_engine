# from src.game import Game
# from src.board import Board
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square
from src.functions.find_moves import find_available_moves

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
    opp_sq_balance = len(sq_white[0]) - len(sq_black[1])
    own_sq_balance = ((len(sq_white[1])-len(sq_white[0])) 
                        + (len(sq_black[1])-len(sq_black[0])))
    eval += 0.5 * opp_sq_balance + 0.25 * own_sq_balance
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

def space_control(game, side):
    # How many squares on the other side of the board
    #   can you attack? 
    # Include squares occupied, empty squares, and 
    #   enemy pieces attacked
    pieces = game.board.white() if side == "white" else game.board.black()
    all_squares = set()
    opponent_squares = set()

    for piece in pieces:
        # look forward for each piece, and see all available moves
        # if a square is on opponent's side of board, add to set
        all_squares.add(piece.square())
        moves = find_available_moves(game, piece) #this is the wrong function to use for pawns
        all_squares.update(moves)
    
    for square in all_squares:
        _, rank = parse_square(square)
        if rank > 4 and side == 'white':
            opponent_squares.add(square)
        elif rank < 5 and side == 'black':
            opponent_squares.add(square)
        
    return opponent_squares, all_squares
