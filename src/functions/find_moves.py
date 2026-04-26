from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square

def find_available_moves(game, piece):
    moves = set()
    boolio = type(piece) == type(Pawn)
    print("Available moves", type(piece), boolio)

    # print("Available moves of", piece)
    match type(piece):
        case Pawn():
            print('tato')
            print(find_pawn_moves(game, piece))
            moves.update(find_pawn_moves(game, piece))
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
