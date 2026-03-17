from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square

def find_available_moves(board, piece):
    moves = set()

    match type(piece):
        case Pawn():
            moves.update(find_pawn_moves(board, piece))
        case King():
            pass
        case Queen():
            pass
        case Bishop():
            pass
        case Rook():
            pass
        case Knight():
            pass

    return moves

def find_pawn_moves(board, pawn):
    moves = []
    file, rank = pawn.file, pawn.rank
    next_rank = rank + 1 if pawn.side == 'white' else rank - 1
    file_idx = board.files.index(file)
    files_to_check =[board.files[j] for j in 
                     [i + file_idx for i in range(-1,2)]
                     if j in range(0,8)]
    for f in files_to_check:
        contents = board.check_square_filled(f, next_rank)
        if f == file and not contents[0]:
            moves.append(f'{f}{next_rank}')
        elif contents[0] and contents[1] != pawn.side:
            moves.append(f'{f}{next_rank}')
    return moves


def find_king_moves(board, pawn):
    pass

def find_knight_moves(board, pawn):
    pass

def find_queen_moves(board, pawn):
    pass

def find_rook_moves(board, pawn):
    pass

def find_bishop_moves(board, pawn):
    pass
