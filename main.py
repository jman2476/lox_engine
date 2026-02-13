from src.board import Board
from src.game import Game
import sys

def main():
    print("Starting new game with lox-engine!")
    fen = sys.argv[1]
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
        move = input('Next move>> ')
        game.parse_move(move)


if __name__ == "__main__":
    main()

 
