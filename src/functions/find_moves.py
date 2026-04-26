from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square

def find_available_moves(game, piece):
    moves = set()
  
    match piece:
        case Pawn():
            moves.update(find_pawn_moves(game, piece))
        case King():
            moves.update(find_king_moves(game, piece))
        case Queen():
            moves.update(find_queen_moves(game, piece))
        case Bishop():
            moves.update(find_bishop_moves(game,piece))
        case Rook():
            moves.update(find_rook_moves(game, piece))
        case Knight():
            moves.update(find_knight_moves(game, piece)) 

    return moves

def find_pawn_moves(game, pawn):
    moves = []
    file, rank = pawn.file, pawn.rank
    direction = 1 if pawn.side == 'white' else  -1
    next_rank = rank + direction
    file_idx = game.board.files.index(file)
    files_to_check =[game.board.files[j] for j in 
                     [i + file_idx for i in range(-1,2)]
                     if j in range(0,8)]
    for f in files_to_check:
        square = f'{f}{next_rank}'
        contents = game.board.check_square_filled(f, next_rank)
        if f == file and not contents[0]:
            moves.append(square)
        elif contents[0] and contents[1] != pawn.side:
            moves.append(square)
        elif not contents[0] and square == game.en_passent:
            moves.append(square)
    double_move = game.board.check_square_filled(f, next_rank + direction)
    if pawn.in_start_pos and not double_move[0]:
        moves.append(f'{file}{next_rank+direction}')
    return moves


def find_king_moves(game, king):
    moves = []
    file, rank = king.file, king.rank
    return moves

def find_knight_moves(game, knight):
    moves = []
    file, rank = knight.file, knight.rank
    return moves

def find_queen_moves(game, queen):
    moves = []
    file, rank = queen.file, queen.rank
    return moves

def find_rook_moves(game, rook):
    moves = []
    file, rank = rook.file, rook.rank
    return moves

def find_bishop_moves(game, bishop):
    moves = []
    file, rank = bishop.file, bishop.rank
    return moves
