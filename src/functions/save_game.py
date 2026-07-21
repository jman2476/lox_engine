import matplotlib.pyplot as plt
import os


def save_game(pgn_path, plt_Figure, game_title):
    dir_path = os.path.abspath(f'./played_games/{game_title}')
    if not os.path.exists(os.path.abspath('./played_games')):
        print('Please install "played_games" submodule from https://github.com/jman2476/lox_engine_game_history as "played_games". If the submodule is installed under a different name, please change the directory name to accomodate.')
        os.mkdir('./tmp_played_games')
        dir_path = os.path.abspath(f'./tmp_played_games/{game_title}')
    os.mkdir(dir_path)