from src.functions.game_writer import read_pgn
from src.game import Game

def game_replay(pgn_file, dir='.'):
    move_list, result = read_pgn(pgn_file, dir)
    game = Game()
    game.board.setup_new()
    game.set_fen()
    move_num = 0
    ply = 0
    print_game_moves(move_list)
    print(game.board)

    while game.winner == None or move_num > len(move_list):
        input('Press return for next move')
        move = move_list[move_num][ply]
        print(f'Move {move_num + 1}')
        print(f'{'white'if ply == 0 else 'black'}\'s move: {move}')
        game.parse_move(move)
        print(game.board)
        print(game.fen)
        move_num += 1 if ply == 1 else 0
        ply += 1
        ply %= 2
        if '-' in move_list[move_num][ply] and '1' in move_list[move_num][ply]:
            set_winner(game, move_list[move_num][ply])
            print(game.board)
            print(f'{game.winner} won the game!')
    print(f'Result: {result}')

def set_winner(game, result):
    print(f'res: {result}')
    if result == '1-0':
        game.winner = 'white'
    elif result == '0-1':
        game.winner = 'black'
    else:
        game.winner = 'Nobody'
        
def print_game_moves(move_list):
    for i in range(0,len(move_list)):
        move = move_list[i]
        if len(move) == 2:
            print(f'{i+1}. {move[0]} {move[1]}')
        else:
            print(f'Result: {move[0]}')