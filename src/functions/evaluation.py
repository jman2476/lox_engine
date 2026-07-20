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
    sq_black, k_atk_black = space_control(board, 'black')
    sq_white, k_atk_white = space_control(board, 'white')
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
    
    ## Currently folded into space_control function as second return
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
    (pieces, opp_pieces) = (board.white(), board.black()) if side == "white" else (board.black(), board.white())
    all_squares = ControlledSquares()
    opponent_squares = ControlledSquares()
    # For calculating king safety concurrent to space_controlled
    opp_king = next((p for p in opp_pieces if p.name == 'king'))
    king_attacks = ControlledSquares() # squares attacked around enemy king are counted again, and count double
    k_file_idx, k_rank_idx = (board.files.index(opp_king.file),
                              opp_king.rank)
    king_adj = [f'{board.files[f]}{r}' for f in 
                [k_file_idx+i for i in range(-1,2)] 
               for r in [k_rank_idx+i for i in range(-1,2)]
               if ((f != k_file_idx or r != k_rank_idx)
                   and f in range(0,8)
                   and r in range(1,9))]

    for piece in pieces:
        # look forward for each piece, and see all available moves
        # if a square is on opponent's side of board, add to set
        all_squares += find_squares_controlled(board, piece)
    
    logger.debug(f'all_squares for {side}: {all_squares}')
    for sq in all_squares.squares:
        logger.debug(f'{sq}, {all_squares.squares[sq]}')
        _, rank = parse_square(sq)
        if rank > 4 and side == 'white':
            opponent_squares.squares[sq] = all_squares.squares[sq]
        elif rank < 5 and side == 'black':
            # opponent_squares.add([sq])
            opponent_squares.squares[sq] = all_squares.squares[sq]
            # logger.debug(f'get opponent squares controlled check: {opponent_squares.squares}')

        # king safety calculation
        if sq in king_adj:
            # logger.debug(f'square in adjacent to enemy king: {sq},\nking_attacks: {king_attacks.squares}')
            # if sq in king_attacks.squares:
            #     logger.debug(f'Square {sq} exists in king_attacks squares')
            for _ in range(all_squares.squares[sq]):
                king_attacks.add([sq, sq])
            # logger.debug(f'king_attacks: {king_attacks}')

    # logger.debug(f'End of space control:\nopponent_sq: {opponent_squares}\nking attacks: {king_attacks}')
    return opponent_squares, king_attacks
