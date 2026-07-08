# Similar to find_moves.py, but finding how many squares are controlled,
#  not what moves a piece can do. Main difference will be for king and pawn
from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.linears import (get_horizontal_squares,
                                   get_vertical_squares)
from src.functions.parse import (parse_square,
                                 parse_square_reverse)
from src.functions.diagonals import get_diagonal_squares
import logging
logger = logging.getLogger(__name__)

class ControlledSquares():
    def __init__(self):
        self.squares = {}

    def __repr__(self):
        string = '{'
        for key in self.squares:
            string += f'{key}: {self.squares[key]}\n'
        return string + '}'

    def add(self, squares:list[str]):
        for sq in squares:
            logger.debug(f'Index: {sq}')
            if sq in self.squares:
                logger.debug(f'Index {sq} found, current value: {self.squares[sq]}')
                self.squares[sq] += 1
            else:
                self.squares[sq] = 1
            logger.debug(f'Index: {sq}, value: {self.squares[sq]}')

    def __add__(self, other):
        #write in overload to combine two objects
        sum = ControlledSquares()
        keys = list(self.squares) + list(other.squares)
        for key in keys:
            sum.squares[key] = (self.squares.get(key, 0) 
                                + other.squares.get(key, 0))
        return sum

def find_squares_controlled(board, piece):
    moves = ControlledSquares()

    match piece:
        case Pawn():
            print(f'pawn squares controlled: {pawn_squares_controlled(board, piece)}')
            moves.add(pawn_squares_controlled(board, piece))
        case King():
            moves.add(king_squares_controlled(board, piece))
        case Queen():
            moves.add(queen_squares_controlled(board, piece))
        case Bishop():
            moves.add(bishop_squares_controlled(board, piece))
        case Rook():
            moves.add(rook_squares_controlled(board, piece))
        case Knight():
            moves.add(knight_squares_controlled(board, piece))
    return moves

def pawn_squares_controlled(board, pawn) -> list[str]:
    file, rank = pawn.file, pawn.rank
    direction = 1 if pawn.side == 'white' else -1
    f_idx = board.files.index(file)
    files_to_check = [board.files[j] for j in 
                      [i + f_idx for i in range(-1,2) 
                       if i != 0] if j in range(0,8)]
    logger.debug(f'{pawn}, {files_to_check}, {rank+direction}, {[f'{f}{rank+direction}' for f in files_to_check]}')
    return [f'{f}{rank+direction}' for f in files_to_check]

def king_squares_controlled(board, king) -> list[str]:
    file, rank = king.file, king.rank
    f_idx = board.files.index(file)
    return [f'{board.files[f]}{r}' for f in [f_idx+i for i in range(-1,2)] 
               for r in [r+i for i in range(-1,2)]
               if f != f_idx or r != rank]


def queen_squares_controlled(board, queen) -> list[str]:
    squares = []
    file, rank, side = queen.file, queen.rank, queen.side
    h_edges = board.bound_squares('horizontal', True)(file, rank, side)
    v_edges = board.bound_squares('vertical', True)(file, rank, side)
    b_edges = board.bound_squares(
        'diagonal', True)(file, rank, side, 'back')
    f_edges = board.bound_squares(
        'diagonal', True)(file, rank, side, 'forward')
    
    b_edge_sqs = [parse_square(sq) for sq in b_edges]
    f_edge_sqs = [parse_square(sq) for sq in f_edges]

    squares.extend([
        *get_horizontal_squares(*h_edges),
        *get_vertical_squares(*v_edges)
    ])

    if b_edges[0] != b_edges[1]:
        squares = get_diagonal_squares(b_edge_sqs[0], b_edge_sqs[1])
        squares.extend(
            [parse_square_reverse(sq) for sq in squares]
        )
    if f_edges[0] != f_edges[1]:
        squares = get_diagonal_squares(f_edge_sqs[0], f_edge_sqs[1])
        squares.extend(
            [parse_square_reverse(sq) for sq in squares]
        )
    
    return squares

def bishop_squares_controlled(board, bishop) -> list[str]:
    file, rank, side = bishop.file, bishop.rank, bishop.side
    b_edges = board.bound_squares('diagonal', True)(file, rank, side, 'back')
    f_edges = board.bound_squares('diagonal', True)(file, rank, side, 'forward')
    b_edges_sq = [parse_square(sq) for sq in b_edges]
    f_edges_sq = [parse_square(sq) for sq in f_edges]
    b_squares, f_squares = [], []
    if b_edges[0] !=  b_edges[1]:
        b_squares = get_diagonal_squares(b_edges_sq[0], b_edges_sq[1])
    if f_edges[0] != f_edges[1]:
        f_squares = get_diagonal_squares(f_edges_sq[0], f_edges_sq[1])

    return [parse_square_reverse(sq) 
             for sq in  [*b_squares, *f_squares]]

def knight_squares_controlled(board, knight) -> list[str]:
    return board.bound_squares('knight', True)(
        knight.file,
        knight.rank,
        knight.side
    )


def rook_squares_controlled(board, rook) -> list[str]:
    file, rank, side = rook.file, rook.rank, rook.side

    h_limits = board.bound_squares('horizontal', True)(file, rank, side)
    v_limits = board.bound_squares('vertical', True)(file, rank, side)

    return [*get_horizontal_squares(*h_limits),
            *get_vertical_squares(*v_limits)]