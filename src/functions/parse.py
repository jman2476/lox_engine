import copy
import re

def parse_square(square_string):
        if len(square_string) > 2:
             raise ValueError('parse_square: square_string is too long, should be 2 characters')
        (file, rank) = (square_string[0], square_string[1])
        if ord(rank) not in range(49, 57):
            raise ValueError('parse_square: rank not between 1 and 8')
        if ord(file) not in range(97, 105) and ord(file) not in range(65, 72):
            raise ValueError('parse_square: file not between a and h, or A and H')
        # print(f'Good square: {file}{ord(rank) - 48}')
        return file.lower(), ord(rank) - 48

def parse_pawn_move(game, string):
    move_board = copy.deepcopy(game.board)
    file, rank = parse_square(string)
    direction = -1 if game.turn == 'white' else 1
    pawn_rank = rank + direction
    piece = move_board.board[file][pawn_rank-1]
    next_pawn_rank = pawn_rank + direction
    two_square_piece = move_board.board[file][next_pawn_rank-1]
    if piece is None:
        if two_square_piece is not None:
            if two_square_piece.name == 'pawn':
                if two_square_piece.side == game.turn and two_square_piece.in_start_pos:
                    two_square_piece.move(move_board, string)
                else:        
                    raise ValueError('Pawn move error: You cannot do that')
            else:         
                raise ValueError('Pawn move error: That is not a pawn')
        else:
            raise ValueError(f'Pawn move error: No pawn found to move to {string}')
    elif piece.name != 'pawn':
        raise ValueError('Pawn move error: piece in previous square is not a pawn')
    elif piece.name == 'pawn':
        if piece.side == game.turn:
            piece.move(move_board, string)
        else:
            raise ValueError(f'Pawn move error: {piece} is not your pawn to move!')
        
    print(f'You did a pawn move: \n', move_board)
    return move_board

def parse_pawn_promotion(game, string):
    move_board = copy.deepcopy(game.board)
    # Regex: /[a-h][18]=[QNRB]/g
    regex = r'[a-h][18]=[QNRB]'
    match = re.match(regex, string)
    print(f'Matched {match} from {string} using {regex}')
    square_seperator = re.match(r'([a-h][18])(=[QNBR])',string)
    print(f'Got square {square_seperator.group(1)} and new piece {square_seperator.group(2)} from {string} using {r'([a-h][18])'}')
    
    if match is None:
        raise ValueError(f'Pawn promotion error: Improper move syntax for pawn promotion {string}')
    elif len(string) == len(match.group(0)):
        print(f'Looks like simple pawn promotion')
    return move_board

def parse_castling(game, pieces, king, checks, string):
    move_board = copy.deepcopy(game.board)
    rooks = [piece for piece in pieces if piece.name == 'rook']
    for rook in rooks:
        print(rook)
    if string in ['0-0', 'O-O', 'o-o']:
        h_rook = next((rook for rook in rooks 
                        if (rook.square == 'h1' or rook.square == 'h8')))
        print(f'a_rook: {h_rook}, {h_rook.in_start_pos}')
        if h_rook is None or not h_rook.in_start_pos:
            raise ValueError(
                'Castling failure: The h rook has been moved off starting square')
        elif not king.in_start_pos:
            raise ValueError(
                'Castling failure: King has moved off of starting square'
            )
        elif len(checks) > 0:
            print(f'Checks: {checks}')
            raise ValueError(
                f'Castling failure: King is in check'
            )
        
        # handle castling
        # will king move through check on f and g files?
        (f_sqr, g_sqr) = ('f' + king.square[1],
                            'g' + king.square[1])
        print(f'Squares to check during castling: {f_sqr}{g_sqr}')
        f_file, f_rank = parse_square(f_sqr)
        g_file, g_rank = parse_square(g_sqr)
        blocked = (move_board.check_square_filled(f_file,f_rank)[0],
                    move_board.check_square_filled(g_file,g_rank)[0])
        if True in blocked:
            raise ValueError(
                'Castling error: Castling movement is blocked by a piece')

        f_check, g_check = (move_board.find_checks(f_sqr, king.side),
                            move_board.find_checks(g_sqr, king.side))
        if len(f_check) > 0 or len(g_check) > 0:
            print(f'Threats on f square: {f_check}')
            print(f'Threats on g square: {g_check}')
            raise ValueError(
                'Castling error: King would move through check to castle')

        move_board.board['g'][g_rank-1] = king
        move_board.board['f'][f_rank-1] = h_rook
        move_board.board[king.file][king.rank-1] = None
        move_board.board[h_rook.file][h_rook.rank-1] = None
        king.square = g_sqr
        h_rook.square = f_sqr
        print(f'Post move board: \n{move_board}')
    elif string in ['0-0-0', 'o-o-o', 'O-O-O']:
        a_rook = next((rook for rook in rooks 
                        if (rook.square == 'a1' or rook.square == 'a8')))
        if a_rook is None or not a_rook.in_start_pos:
            print(f'a_rook: {a_rook}, {a_rook.in_start_pos}')
            raise ValueError(
                'Castling failure: The a rook has been moved off starting square')
        elif not king.in_start_pos:
            raise ValueError(
                'Castling failure: King has moved off of starting square'
            )
        elif len(checks) > 0:
            print(f'Checks: {checks}')
            raise ValueError(
                f'Castling failure: King is in check'
            )
        
        # handle castling
        # will king move through check on f and g files?
        (d_sqr, c_sqr) = ('d' + king.square[1],
                            'c' + king.square[1])
        print(f'Squares to check during castling: {d_sqr}{c_sqr}')
        d_file, d_rank = parse_square(d_sqr)
        c_file, c_rank = parse_square(c_sqr)
        blocked = (move_board.check_square_filled(d_file,d_rank)[0],
                    move_board.check_square_filled(c_file,c_rank)[0])
        if True in blocked:
            raise ValueError(
                'Castling error: Castling movement is blocked by a piece')

        d_check, c_check = (move_board.find_checks(d_sqr, king.side),
                            move_board.find_checks(c_sqr, king.side))
        if len(d_check) > 0 or len(c_check) > 0:
            print(f'Threats on d square: {d_check}')
            print(f'Threats on c square: {c_check}')
            raise ValueError(
                'Castling error: King would move through check to castle')

        move_board.board['c'][c_rank-1] = king
        move_board.board['d'][d_rank-1] = a_rook
        move_board.board[king.file][king.rank-1] = None
        move_board.board[a_rook.file][a_rook.rank-1] = None
        king.square = c_sqr
        a_rook.square = d_sqr
        print(f'Post move board: \n{move_board}')
    else:
        raise ValueError(
            'Invalid move syntax. Suspected castling move.')