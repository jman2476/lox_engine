from src.piece import (
    Pawn, King, 
    Queen, Bishop, 
    Knight, Rook
    )
from src.functions.parse import (parse_square,
                                 parse_piece_move, 
                                 parse_square_reverse,
                                 parse_pawn_move,
                                 parse_pawn_capture)
from src.functions.direction import adjacent_squares
from src.functions.linears import (get_horizontal_squares,
                                   get_vertical_squares)
from src.functions.diagonals import get_diagonal_squares
import copy
import logging
from time import sleep
from datetime import datetime
logger = logging.getLogger(__name__)
logging.basicConfig(filename='lox_engine.log', level=logging.DEBUG, filemode='w')
# loggerinfo(f'Starting log {datetime.now()}')


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

def find_move_notation(game, piece):
    notation = []

    match piece:
        case Pawn():
            moves = find_pawn_moves(game, piece)
            for mv in moves:
                file, rank = parse_square(mv[:2])
                if (game.board.check_square_filled(file, rank)[0]
                    or mv == game.en_passent):
                    notation.append(f'{piece.file}x{mv}')
                else:
                    notation.append(mv)
        case King():
            moves = find_king_moves(game, piece)
            for mv in moves:
                if len(mv) > 2:
                    notation.append(mv)
                    continue
                file, rank = parse_square(mv)
                if game.board.check_square_filled(file, rank)[0]:
                    notation.append(f'Kx{mv}')
                else:
                    notation.append(f'K{mv}')
        case Queen():
            moves = find_queen_moves(game, piece)
            for mv in moves:
                file, rank = parse_square(mv)
                if game.board.check_square_filled(file, rank)[0]:
                    notation.append(f'Q{piece.square()}x{mv}')
                else:
                    notation.append(f'Q{piece.square()}{mv}')
        case Bishop():
            moves = find_bishop_moves(game,piece)
            for mv in moves:
                file, rank = parse_square(mv)
                if game.board.check_square_filled(file, rank)[0]:
                    notation.append(f'B{piece.square()}x{mv}')
                else:
                    notation.append(f'B{piece.square()}{mv}')
        case Rook():
            moves = find_rook_moves(game, piece)
            for mv in moves:
                file, rank = parse_square(mv)
                if game.board.check_square_filled(file, rank)[0]:
                    notation.append(f'R{piece.square()}x{mv}')
                else:
                    notation.append(f'R{piece.square()}{mv}')
        case Knight():
            moves = find_knight_moves(game, piece)
            for mv in moves:
                file, rank = parse_square(mv)
                if game.board.check_square_filled(file, rank)[0]:
                    notation.append(f'N{piece.square()}x{mv}')
                else:
                    notation.append(f'N{piece.square()}{mv}') 

    return notation 


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
    
    # check for two square move:
    # print(f'Checking two square move: {game.board.check_square_filled(file, next_rank + direction)}')
    if (pawn.in_start_pos and
        f'{file}{next_rank}' in moves and
        not game.board.check_square_filled(file, next_rank + direction)[0]):
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
                # logger.debug(f'find pawn move: {mv}')
                gm.parse_move(mv, False)
            else:
                # logger.debug(f'find pawn move: {file}x{mv}')
                gm.parse_move(f'{file}x{mv}', False)

            if gm.fen != game.fen:
                valid_moves.append(mv)
        except Exception as e:
            print(f'Move {mv} failed: {str(e)}')
            continue
        gm = None

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
        move_str = ''
        dst_occupied, dst_side, _ = game.board.check_square_filled(file, rank)
        if dst_occupied:
            if dst_side == king.side: continue
            else: 
                move_str = f'Kx{square}'
        else:
            move_str = f'K{square}'
        move_board, _ = parse_piece_move(game, move_str)
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
    moves = game.board.bound_squares('knight')(
        knight.file,
        knight.rank,
        knight.side
    )
    return validate_legal_moves(game, knight, moves)

def find_queen_moves(game, queen):
    side = queen.side
    file, rank = queen.file, queen.rank
    moves = []
    h_edges = game.board.bound_squares('horizontal')(file, rank, side)
    v_edges = game.board.bound_squares('vertical')(file, rank, side)
    b_edges = game.board.bound_squares('diagonal')(
        file, rank, side, 'back')
    f_edges = game.board.bound_squares('diagonal')(
        file, rank, side, 'forward')

    b_edge_sqs = [parse_square(sq) for sq in b_edges]
    f_edge_sqs = [parse_square(sq) for sq in f_edges]
    
    moves.extend([
        *get_horizontal_squares(*h_edges),
        *get_vertical_squares(*v_edges)
    ])

    if b_edges[0] != b_edges[1]:
        squares = get_diagonal_squares(b_edge_sqs[0], b_edge_sqs[1])
        moves.extend(
            [parse_square_reverse(sq) for sq in squares]
        )
    if f_edges[0] != f_edges[1]:
        squares = get_diagonal_squares(f_edge_sqs[0], f_edge_sqs[1])
        moves.extend(
            [parse_square_reverse(sq) for sq in squares]
        )

    return validate_legal_moves(game, queen, moves)

def find_rook_moves(game, rook):
    side = rook.side
    file, rank = parse_square(rook.square())

    h_limits = game.board.bound_squares('horizontal')(file, rank, side)
    v_limits = game.board.bound_squares('vertical')(file, rank, side)

    h_squares = get_horizontal_squares(*h_limits)
    v_squares = get_vertical_squares(*v_limits)

    return validate_legal_moves(game, rook, [*h_squares, *v_squares])

def find_bishop_moves(game, bishop):
    moves = []
    side = bishop.side
    file, rank = bishop.file, bishop.rank
    b_edges = game.board.bound_squares('diagonal')(file, rank, side, 'back')
    f_edges = game.board.bound_squares('diagonal')(file, rank, side, 'forward')
    b_edges_sq = [parse_square(sq) for sq in b_edges]
    f_edges_sq = [parse_square(sq) for sq in f_edges]
    b_squares, f_squares = [], []
    if b_edges[0] !=  b_edges[1]:
        b_squares = get_diagonal_squares(b_edges_sq[0], b_edges_sq[1])
    if f_edges[0] != f_edges[1]:
        f_squares = get_diagonal_squares(f_edges_sq[0], f_edges_sq[1])

    moves = [parse_square_reverse(sq) 
             for sq in  [*b_squares, *f_squares]]
    
    return validate_legal_moves(game, bishop, moves)

# Take in all possible squares, return list of moves
# that don't put your king in check
def validate_legal_moves(game, piece, moves):
    letter = {
        'queen': 'Q',
        'rook': 'R',
        'knight': 'N',
        'bishop': 'B'
    }
    valid_moves = []
    start_sq = f'{letter[piece.name]}{piece.file}{piece.rank}'

    for mv in moves:
        if mv == start_sq[1:]:
            continue
        gm = copy.deepcopy(game)
        capture, _, __ = gm.board.check_square_filled(*parse_square(mv))
        mv_str = f'{start_sq}{'x' if capture else ''}{mv}'
        try:
            # logger.debug(f'validate legal moves: {mv_str}')
            gm.parse_move(mv_str, False)
            # if gm.fen != game.fen:
            # logger.debug(f'{game} {piece} {moves}')
            
            if game.fen != gm.fen:
                valid_moves.append(mv)
        except Exception as e:
            print(f'Move {mv} as {mv_str} failed: {str(e)}')

    return valid_moves

# Compare fen strings on character at a time:
def fen_compare(pre_move:str, post_move:str) -> bool:
    # logger.debug(f'Comparing fen strings {pre_move} and {post_move}')

    return pre_move == post_move