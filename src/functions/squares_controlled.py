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
class ControlledSquares():
    def __init__(self):
        self.squares = {}

    def add(self, squares:list[str]):
        for sq in squares:
            if sq in self.squares:
                self.squares[sq] += 1
            else:
                self.squares[sq] = 1

def find_squares_controlled(board, piece):
    moves = ControlledSquares()

    match piece:
        case Pawn():
            moves.add(pawn_squares_controlled(board, piece))
        case King():
            moves.update(king_squares_controlled(board, piece))
        case Queen():
            moves.update(queen_squares_controlled(board, piece))
        case Bishop():
            moves.update(bishop_squares_controlled(board, piece))
        case Rook():
            moves.update(rook_squares_controlled(board, piece))
        case Knight():
            moves.update(knight_squares_controlled(board, piece))
    return moves

def pawn_squares_controlled(board, pawn) -> list[str]:
    file, rank = pawn.file, pawn.rank
    direction = 1 if pawn.side == 'white' else -1
    f_idx = board.files.index(file)
    files_to_check = [board.files[j] for j in 
                      [i + f_idx for i in range(-1,2) 
                       if i != 0] if j in range(0,8)]
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
    file, rank, side = parse_square(rook.square()), rook.side

    h_limits = board.bound_squares('horizontal', True)(file, rank, side)
    v_limits = board.bound_squares('vertical', True)(file, rank, side)

    return [*get_horizontal_squares(*h_limits),
            *get_vertical_squares(*v_limits)]