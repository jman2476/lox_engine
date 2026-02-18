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
        return file.lower(), int(rank)

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
                    game.en_passent = f'{file}{rank + direction}'
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

def parse_pawn_capture(game, string):
    move_board = copy.deepcopy(game.board)
    regex = r'^([a-h][xX])([a-h][2-7])'
    match = re.match(regex, string)
    direction = -1 if game.turn == 'white' else 1

    if match is None:
        raise ValueError(
            'Pawn capture error: Improper capture syntax. If capturing on ranks 1 or 8, must specify piece to promote to (e.g. "=Q")')
    else:
        prev_file = string[0]
        square = string[-2:]
        file, rank = parse_square(square)
        piece_at_target = move_board.check_square_filled(file, rank)
        attack_pawn = move_board.check_square_filled(prev_file, rank + direction)

        if not piece_at_target[0]:
            raise ValueError(
                f'Pawn capture error: No piece to capture at {square}'
            )
        elif piece_at_target[1] == game.turn:
            raise ValueError(
                f'Pawn capture error: You cannot capture your own piece at {square}'
            )
        elif (not attack_pawn[0] 
              or attack_pawn[1] != game.turn
              or attack_pawn[2].name != 'pawn'):
            raise ValueError(
                f'Pawn capture error: You don\'t have a pawn to capture on {square} with at {prev_file}{rank + direction}'
            )
        move_board.board[file][rank-1] = attack_pawn[2]
        move_board.board[prev_file][rank+direction-1] = None

    return move_board

def parse_pawn_promotion(game, string):
    move_board = copy.deepcopy(game.board)
    # Regex: /[a-h][18]=[QNRB]/g
    regex = r'[a-h][18]=[QNRB]'
    match = re.search(regex, string)
    print(f'Matched {match} from {string} using {regex}')
    square_seperator = re.search(r'([a-h][18])(=[QNBR])',string)
    # print('Tato', square_seperator)
    print(f'Got square {square_seperator.group(1)} and new piece {square_seperator.group(2)} from {string} using {r'([a-h][18])'}')
    # print('Scopo')
    file, rank = parse_square(square_seperator.group(1))
    
    if match is None:
        raise ValueError(f'Pawn promotion error: Improper move syntax for pawn promotion {string}')
    elif len(string) == len(match.group(0)):
        print(f'Looks like simple pawn promotion')
        if move_board.check_square_filled(file, rank-1)[0]:
            raise ValueError(f'Promotion error: square {file}{rank} is occupied.')
        print(f'Rank: {rank}, file: {file}, turn: {game.turn}')
        if rank == 8 and game.turn == 'white':
            prv_sq_filled, __, piece = move_board.check_square_filled(file, 7)
            if prv_sq_filled and piece.name == 'pawn':
                new_piece = move_board._fen_piece[string[-1]]('white', f'{file}8')
                move_board.board[file][7] = new_piece
                move_board.board[file][6] = None
            else:
                raise ValueError(f'Promotion Error: No pawn to promote at {file}7')
        elif rank == 1 and game.turn == 'black':
            prv_sq_filled, __, piece = move_board.check_square_filled(file, 2)
            if prv_sq_filled and piece.name == 'pawn':
                new_piece = move_board._fen_piece[string[-1]]('black', f'{file}1')
                move_board.board[file][0] = new_piece
                move_board.board[file][1] = None
            else:
                raise ValueError(f'Promotion Error: No pawn to promote at {file}2')
        else:
            raise ValueError(f'Promotion error: {game.turn.title()} cannot promote on square {square_seperator.group(1)}')
    elif 'x' in string or 'X' in string:
        prev_file = string[0]
        prev_rank = 7 if game.turn == 'white' else 2
        capture_square = move_board.check_square_filled(file, rank)
        if not capture_square[0]:
            raise ValueError(f'Promotion error: No piece to capture at {file}{rank}')
        elif capture_square[1] == game.turn:
            raise ValueError(f'Promotion error: You cannot capture your own piece at {file}{rank}')
        else: 
            prv_sq_filled, __, piece = move_board.check_square_filled(prev_file, prev_rank)
            if not prv_sq_filled or piece.name != 'pawn':
                raise ValueError(f'Promotion error: No pawn to move at {prev_file}{prev_rank}')
            if game.turn == 'white':
                new_piece = move_board._fen_piece[string[-1]]('white', f'{file}8')
                move_board.board[file][7] = new_piece
                move_board.board[prev_file][prev_rank-1] = None
            else:
                new_piece = move_board._fen_piece[string[-1]]('black', f'{file}1')
                move_board.board[file][0] = new_piece
                move_board.board[prev_file][prev_rank-1] = None
    print('Done parsing pawn promotion\n', move_board)
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
    
def parse_piece_move(game, string):
    # print('po')
    move_board = copy.deepcopy(game.board)
    piece_type = move_board._fen_piece[string[0]]
    regex = r'^([BKNRQ])([a-h]*[1-8]*)(x*)([a-h][1-8])$'
    matches = re.match(regex, string)
    disambiguation = matches.groups()[1]
    capture = matches.groups()[2]
    square = matches.groups()[3]
    file, rank = parse_square(square)
    
    print(f'Match groups {matches.groups()}')
    print(f'Moving {piece_type} to {square}')
    print(f'Disambiguation code: {disambiguation or 'None'}')
    # print(f'Capture? {capture=='x'}')
    # Check what type of move it is:
    #   - Basic move: Be5
    #   - Basic capture: Bxe5
    #   - Disambiguated moves:
        #   - Single disambiguated: Ree4/R4e4
        #   - Single dis capture: Rexe4
        #   - Double disambiguated: Re1e4
        #   - Double dis capture: Re1xe4
    if square:
        destination_square = move_board.check_square_filled(file, rank)
        pieces = piece_lookback(move_board, string[0], square)
        piece = None
        print('Pieces found',pieces)
        for p in pieces:
            if p is None:
                continue
            if p.side == game.turn and isinstance(p, piece_type):
                if piece and disambiguation == '':
                    raise ValueError(f'Piece move error: Multiple {piece_type}s can move to {square}: at least {piece} and {p}. Please disambiguate the move')
                elif disambiguation != '':
                    print(f'{p}: file {p.file}, rank {p.rank}')
                    if disambiguation in move_board.files:
                        if p.file == disambiguation:
                            piece = p
                        else: continue
                    elif int(disambiguation) in move_board.ranks:
                        print(f'disambigs: {int(disambiguation)}')
                        if p.rank ==int(disambiguation):
                            piece = p
                        else: continue
                    else:
                        if p.square == disambiguation:
                            piece = p
                else:
                    print(f'Piece found: {p}')
                    piece = p
        if piece:
            print('Piece', piece)
            if destination_square[0] and destination_square[1] == game.turn:
                raise ValueError(f'Piece move error: Cannot capture own {destination_square[2]}')
            elif destination_square[0] and capture != 'x':
                raise ValueError(f'Piece move error: Destination square {square} is occupied; incorrect move syntax')
            else:
                print(f'Moving {piece} to {square}')
                piece.move(move_board, square)
        else:
            raise ValueError(f'Piece move error: No {piece_type} found that can move to {square}')
            
    else:
        raise ValueError(f'Piece move error: No destination square found')

    return move_board

def piece_lookback(board, piece_letter, square):
    directions = {
        'B': ['back_diagonal',
            'forward_diagonal'],
        'N': ['knight'],
        'Q': ['horizontal',
            'vertical',
            'back_diagonal',
            'forward_diagonal'],
        'R': ['horizontal',
            'vertical'],
        'K': ['king']
    }
    pieces = []
    f, r = parse_square(square)

    for dir in directions[piece_letter]:
        next_pieces = board.next_piece(dir)(f, r)
        for piece in next_pieces:
            if piece:
                pieces.append(piece)

    return pieces