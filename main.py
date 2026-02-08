from src.board import Board
from src.game import Game

def main():
    print("Starting new game with lox-engine!")
    game = Game() 
    game.board.setup_new()
    print(game.board)


if __name__ == "__main__":
    main()
