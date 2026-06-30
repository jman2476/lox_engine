import unittest
from src.game import Game
from src.functions.find_moves import (
        find_available_moves,
        find_pawn_moves,
        find_king_moves,
        find_knight_moves,
        find_rook_moves,
        find_bishop_moves,
        find_queen_moves
        )
from src.piece import (
        Pawn, King,
        Queen, Bishop,
        Knight, Rook
        )

class TestFindMoves(unittest.TestCase):
    def test_find_available(self):
        print('==Test: Find available moves, game start==')
        try:
            game = Game()
            game.start_new_game()
            w_pieces = game.board.white()
            moves = []
            for piece in w_pieces:
                moves.append([piece, find_available_moves(game, piece)])

            print("---Available moves:---")
            for piece_moves in moves:
                print(piece_moves[0], piece_moves[1])
        except Exception as e:
            print(f'test_find_available error: ', e)

    def test_find_pawn_moves(self):
        print('==Test: find pawn moves==')
        game = Game()
        game.start_new_game()
        w_pawns = [pawn for pawn in game.board.white() if isinstance(pawn, Pawn)]
        b_pawns = [pawn for pawn in game.board.black() if isinstance(pawn, Pawn)]

        print('-----initial position-----')
        for pawn in w_pawns:
            moves = find_pawn_moves(game, pawn)
            print(f'moves for {pawn}: {moves}')
        
        game.parse_move('e4')
        game.parse_move('d5')
        game.parse_move('a4')
        game.parse_move('b5')
        game.parse_move('e5')
        game.parse_move('f5')
        w_pawns = [pawn for pawn in game.board.white() if isinstance(pawn, Pawn)]
        
        print('---moves: e4, d5, a4, b5, e5, f5---')
        for pawn in w_pawns:
            moves = find_pawn_moves(game, pawn)
            print(f'moves for {pawn}: {moves}')
            
        for pawn in b_pawns:
            moves = find_pawn_moves(game, pawn)
            print(f'moves for {pawn}: {moves}')
        
        print(game.board)

        print('-----second test-----')
        game2 = Game()
        game2.start_new_game()
        w_pawns = [pawn for pawn in game2.board.white() if isinstance(pawn, Pawn)]
        b_pawns = [pawn for pawn in game2.board.black() if isinstance(pawn, Pawn)]
        move_list = ['e4', 'e5', 'Bb5', 'c5', 'h4', 'c4', 'h5', 'c3', 'h6', 'cxb2', 'hxg7', 'a6']

        for pawn in w_pawns:
            moves = find_pawn_moves(game2, pawn)
            print(f'moves for {pawn}: {moves}')
        
        for mv in move_list:
            game2.parse_move(mv)
        
        print("----After moves------")
        #print(f'FEN: {game2.fen}')
        for pawn in [pawn for pawn in game2.board.white() if isinstance(pawn, Pawn)]:
            moves = find_pawn_moves(game2, pawn)
            print(f'moves for {pawn}: {moves}')

        game2.parse_move('Rh5')
        print(f'FEN: {game2.fen}')
        for pawn in [pawn for pawn in game2.board.black() if isinstance(pawn, Pawn)]:
            moves = find_pawn_moves(game2, pawn)
            print(f'moves for {pawn}: {moves}')
        
        print(game2.board)


    def test_find_king_moves(self):
        print('==Test: Find king moves==')
        game = Game()
        game.start_new_game()
        w_king = [king for king in game.board.white() if isinstance(king, King)]
        b_king = [king for king in game.board.black() if isinstance(king, King)]
        move_list = ['e4', 'e5', 'd4', 'Bb4', 'Bd2', 'Nf6', 'h3', 'h6', 'Bxb4', 'd6', 'Qg4', 'a6', 'Nd2', 'O-O', 'O-O-O']
        move_list_2 = ['e4', 'e5', 'Ke2', 'Ke7']
        white_move = True

        def print_w_king_moves(): 
            for king in [king for king in game.board.white() if isinstance(king, King)]:
                moves = find_king_moves(game, king)
                print(f'moves for {king}: {moves}')

        def print_b_king_moves():
            for king in [king for king in game.board.black() if isinstance(king, King)]:
                moves = find_king_moves(game, king)
                print(f'moves for {king}: {moves}')

        print('-------Game start-------')
        print_w_king_moves()

        for mv in move_list:
            print(f'----------move: {mv}----------')
            game.parse_move(mv)
            if white_move:
                print_b_king_moves()
            else:
                print_w_king_moves()
            white_move = not white_move

    def test_find_knight_moves(self):
        print('==Test: Find knight moves==')
        game = Game()
        game.start_new_game()
        move_list = ['Nh3', 'e6', 'f3', 'Qh4', 'Nf2', 'b6']
        
        def print_w_knight_moves():
            for knight in [n for n in game.board.white() 
                           if isinstance(n, Knight)]:
                moves = find_knight_moves(game, knight)
                print(f'moves for {knight}: {moves}')

        for i in range(0, len(move_list)):
            print(f'-----------move: {move_list[i]}-----------')
            game.parse_move(move_list[i])
            if i == 3:
                print_w_knight_moves()
        
        print_w_knight_moves()

    def test_find_rook_moves(self):
        print('==Test: Find rook moves==')
        game = Game()
        game.start_new_game()
        move_list = ['a4', 'a5', 'Ra3', 'Ra6', 'Re3', 'Rd6', 'Rxe7']

        def print_w_rook_move():
            for rook in [r for r in game.board.white()
                         if isinstance(r, Rook)]:
                moves = find_rook_moves(game, rook)
                print(f'moves for {rook}: {moves}')
                
        def print_b_rook_move():
            for rook in [r for r in game.board.black()
                         if isinstance(r, Rook)]:
                moves = find_rook_moves(game, rook)
                print(f'moves for {rook}: {moves}')

        for i in range(0, len(move_list)):
            print(f'--------move: {move_list[i]}-------')
            game.parse_move(move_list[i])
            if i%2 == 0:
                print_b_rook_move()
            else:
                print_w_rook_move()

    def test_find_bishop_moves(self):
        print('==Test: Find bishop moves==')
        game = Game()
        game.start_new_game()
        move_list = ['b3', 'g6', 'g3', 'Bg7', 'Bg2', 'b6', 'Bb2', 'Bb7', 'e4', 'h5']

        def print_b_bishop_move():
            for bishop in [b for b in game.board.black()
                           if isinstance(b, Bishop)]:
                moves = find_bishop_moves(game, bishop)
                print(f'moves for {bishop}: {moves}')

        def print_w_bishop_move():
            for bishop in [b for b in game.board.white()
                           if isinstance(b, Bishop)]:
                moves = find_bishop_moves(game, bishop)
                print(f'moves for {bishop}: {moves}')

        for i in range(0, len(move_list)):
            print(f'--------move: {move_list[i]}-------')
            game.parse_move(move_list[i])
            if i%2 == 0:
                print_b_bishop_move()
            else:
                print_w_bishop_move()

    def test_find_queen_moves(self):
        print('==Test: Find queen moves==')
        game = Game()
        game.start_new_game()
        move_list = ['e4', 'd5', 'Qg4', 'dxe4', 'Qxe4']

        def print_b_queen_move():
            for queen in [q for q in game.board.black()
                           if isinstance(q, Queen)]:
                moves = find_queen_moves(game, queen)
                print(f'moves for {queen}: {moves}')

        def print_w_queen_move():
            for queen in [q for q in game.board.white()
                           if isinstance(q, Queen)]:
                moves = find_queen_moves(game, queen)
                print(f'moves for {queen}: {moves}')

        for i in range(0, len(move_list)):
            print(f'--------move: {move_list[i]}-------')
            game.parse_move(move_list[i])
            if i%2 == 0:
                print_b_queen_move()
            else:
                print_w_queen_move()