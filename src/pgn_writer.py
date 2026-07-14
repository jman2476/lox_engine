import os
import datetime as dt


class PGNWriter():
    def __init__(self, game, dir:str='./recent_games'):
        self.game = game
        self.event = ''
        self.site = 'Lox Engine'
        self.date = dt.datetime.now()
        self.round = '1'
        self.white = game.w_player
        self.black = game.b_player
        self.result = '-'
        self.title = f'{self.white} v {self.black}-{self.date.date()}-{self.date.time()}.pgn'
        self.path = os.path.join(self.set_path(dir), self.title)
        self.turn = 1

    def create_file(self):
        with open(self.path, 'w', encoding='UTF-8') as file:
            file.write(self.format_header())

    def set_path(self, dir:str):
        abs_dir_path = os.path.abspath(dir)
        if not os.path.exists(abs_dir_path):
            os.mkdir(abs_dir_path)
        return abs_dir_path
    
    def format_header(self):
        header = [
            f'[Event "{self.event}"]',
            f'[Site "{self.site}"]',
            f'[Date "{self.date.date()}"]',
            f'[Round "{self.round}"]',
            f'[White "{self.white}"]',
            f'[Black "{self.black}"]',
            f'[Result "{self.result}"]\n'
        ]
        return '\n'.join(header)

    def add_move(self, move:str):
        with open(self.path, 'a', encoding='UTF-8') as f:
            if self.game.turn == 'white':
                f.write(f'{self.game.fullmove}. {move} ')
            else:
                f.write(f'{move} ')

    
    def final_result(self):
        self.result = self.game.winner
        new_header = self.format_header()
        
        with open(self.path, 'r') as f:
            contents = f.read()
        
        move_list = contents.split('"]').pop()

        with open(self.path, 'w', encoding='UTF-8') as f:
            f.write(f'{new_header}{move_list} {self.result}')
