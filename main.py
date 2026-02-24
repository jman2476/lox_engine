from src.board import Board
from src.game import Game
import sys
from colorama import just_fix_windows_console

def main():
    just_fix_windows_console()
    print("Starting new game with lox-engine!")
    print("Please input moves with proper algebraic notation")
    fen = sys.argv[1] if len(sys.argv) > 1 else None
    game = Game() 
    if fen is None:
        game.board.setup_new()
        game.set_fen()
    else: 
        game.read_fen(fen)
        game.set_fen()
    while(game.winner == None):
        print(game.board)
        print(game.fen)
        move = input(f'{game.turn}\'s next move>> ')
        game.parse_move(move)


if __name__ == "__main__":
    main()

 
