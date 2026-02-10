from src.board import Board
from src.game import Game

def main():
    print("Starting new game with lox-engine!")
    game = Game() 
    game.board.setup_new()
    game.set_fen()
    # while(game.winner == None):
    #     print(game.board)
    #     print(game.fen)
    #     move = input()
    #     game.parse_move(move)


if __name__ == "__main__":
    main()

 
