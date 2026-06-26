import unittest
from src.game import Game
from src.functions.find_moves import (
        find_available_moves,
        find_pawn_moves,
        find_king_moves
        )
from src.piece import (
        Pawn, King,
        Queen, Bishop
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
        
    def test_find_king_moves(self):
        print('==Test: Find king moves==')
        game = Game()
        game.start_new_game()
        w_king = [king for king in game.board.white() if isinstance(king, King)]
        b_king = [king for king in game.board.black() if isinstance(king, King)]
        
        print('-------Game start-------')
        for king in w_king:
            moves = find_king_moves(game, king)
            print(f'moves for {king}: {moves}')
        
        print('----------move: e4----------')
        game.parse_move('e4')

        for king in b_king:
            moves = find_king_moves(game, king)
            print(f'moves for {king}: {moves}')
            
        print('----------move: e5----------')
        game.parse_move('e5')

        for king in w_king:
            moves = find_king_moves(game, king)
            print(f'moves for {king}: {moves}')
        
        print('----------move: d4----------')
        game.parse_move('d4')
        for king in b_king:
            moves = find_king_moves(game, king)
            print(f'moves for {king}: {moves}')