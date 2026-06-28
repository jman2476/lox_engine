from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import parse_square, parse_piece_move, parse_pawn_move, parse_pawn_capture
from src.functions.direction import adjacent_squares
import copy

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
        elif (f != file
              and contents[0] 
              and contents[1] != pawn.side):
            moves.append(square)
        elif not contents[0] and square == game.en_passent:
            moves.append(square)
    
    # adjust logic to avoid unnecessary checks
    double_move = game.board.check_square_filled(file, next_rank + direction)
    if pawn.in_start_pos and not double_move[0]:
        moves.append(f'{file}{next_rank+direction}')

    # Check if each move causes check
    valid_moves = []
    for mv in moves:
        gm = copy.deepcopy(game)
        try:
            back_rank = '8' if pawn.side == 'white' else '1'

            if mv[1] == back_rank:
                mv = f'{mv}=Q'

            if mv[0] == file:
                gm.parse_move(mv)
            else:
                gm.parse_move(f'{file}x{mv}')

            if gm.fen != game.fen:
                valid_moves.append(mv)
        except Exception as e:
            print(f'Move {mv} failed: {str(e)}')
            continue

    # Check for promotions
    all_valid = []
    promotions = ['R', 'N', 'B']
    for mv in valid_moves:
        all_valid.append(mv)
        if mv[-1] == 'Q':
            for p in promotions:
                all_valid.append(f'{mv[:2]}={p}')
    return all_valid


def find_king_moves(game, king):
    moves = []
    squares_to_check = adjacent_squares(
        game.board, king.file, king.rank)
    for square in squares_to_check:
        file, rank = parse_square(square)
        dst_occupied, dst_side, _ = game.board.check_square_filled(file, rank)
        if dst_occupied and dst_side == king.side: continue;

        move_board = parse_piece_move(game, f'K{square}')
        checks = move_board.find_checks(square, king.side)
        if len(checks) == 0:
            moves.append(square)

    match king.side:
        case 'white':
            if 'K' in game.castling:
                (f_sqr, g_sqr) = ('f' + king.square()[1],
                            'g' + king.square()[1])
                f_file, f_rank = parse_square(f_sqr)
                g_file, g_rank = parse_square(g_sqr)
                f_check, g_check = (
                    game.board.find_checks(f_sqr, king.side),
                    game.board.find_checks(g_sqr, king.side)
                    )
                blocked = (
                    game.board.check_square_filled(f_file,f_rank)[0],
                    game.board.check_square_filled(g_file,g_rank)[0]
                    )
                if (True not in blocked
                    and len(g_check) == 0
                    and len(f_check) == 0
                    ):
                    moves.append('O-O')
            if 'Q' in game.castling:
                (d_sqr, c_sqr, b_sqr) = ('d' + king.square()[1],
                                'c' + king.square()[1],
                                'b' + king.square()[1])
                d_file, d_rank = parse_square(d_sqr)
                c_file, c_rank = parse_square(c_sqr)
                b_file, b_rank = parse_square(b_sqr)
                d_check, c_check = (
                    game.board.find_checks(d_sqr, king.side),
                    game.board.find_checks(c_sqr, king.side)
                    )
                blocked = (
                    game.board.check_square_filled(d_file,d_rank)[0],
                    game.board.check_square_filled(c_file,c_rank)[0],
                    game.board.check_square_filled(b_file,b_rank)[0]
                    )
                if (True not in blocked
                    and len(d_check) == 0
                    and len(c_check) == 0
                    ):
                    moves.append('O-O-O')
        case 'black':
            if 'k' in game.castling:
                (f_sqr, g_sqr) = ('f' + king.square()[1],
                            'g' + king.square()[1])
                f_file, f_rank = parse_square(f_sqr)
                g_file, g_rank = parse_square(g_sqr)
                f_check, g_check = (
                    game.board.find_checks(f_sqr, king.side),
                    game.board.find_checks(g_sqr, king.side)
                    )
                blocked = (
                    game.board.check_square_filled(f_file,f_rank)[0],
                    game.board.check_square_filled(g_file,g_rank)[0]
                    )
                if (True not in blocked
                    and len(g_check) == 0
                    and len(f_check) == 0
                    ):
                    moves.append('O-O')
            if 'q' in game.castling:
                (d_sqr, c_sqr, b_sqr) = ('d' + king.square()[1],
                                'c' + king.square()[1],
                                'b' + king.square()[1])
                d_file, d_rank = parse_square(d_sqr)
                c_file, c_rank = parse_square(c_sqr)
                b_file, b_rank = parse_square(b_sqr)
                d_check, c_check = (
                    game.board.find_checks(d_sqr, king.side),
                    game.board.find_checks(c_sqr, king.side)
                    )
                blocked = (
                    game.board.check_square_filled(d_file,d_rank)[0],
                    game.board.check_square_filled(c_file,c_rank)[0],
                    game.board.check_square_filled(b_file,b_rank)[0]
                    )
                if (True not in blocked
                    and len(d_check) == 0
                    and len(c_check) == 0
                    ):
                    moves.append('O-O-O')

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
