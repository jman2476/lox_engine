import os
import datetime as dt
import logging
logger = logging.getLogger(__name__)

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
        self.line_length = 0

    def create_file(self):
        with open(self.path, 'w', encoding='UTF-8') as file:
            file.write(self.format_header())

    def set_path(self, dir:str):
        abs_dir_path = os.path.abspath(dir)
        if not os.path.exists(abs_dir_path):
            os.mkdir(abs_dir_path)
        return abs_dir_path
    
    def __reset_players__(self):
        self.white = self.game.w_player
        self.black = self.game.b_player
    
    def format_header(self):
        self.__reset_players__()
        header = [
            f'[Event "{self.event}"]',
            f'[Site "{self.site}"]',
            f'[Date "{self.date.date()}"]',
            f'[Round "{self.round}"]',
            f'[White "{self.white}"]',
            f'[Black "{self.black}"]',
            f'[Result "{self.result}"]\n\n'
        ]
        return '\n'.join(header)

    def add_move(self, move:str, is_check:bool=False):
        # logger.debug(f'adding move {move}')
        append = (f'{self.game.fullmove}. {move} '
                  if self.game.turn == 'white'
                  else f'{move} ')
        chars = len(append)

        if is_check:
            append = append.strip() + '+ '

        with open(self.path, 'a', encoding='UTF-8') as f:
            if chars + self.line_length > 60:
                f.write(f'\n{append}')
                self.line_length = 0
            else:
                f.write(append)
                self.line_length += chars

    
    def final_result(self):
        self.result = self.game.winner
        new_header = self.format_header()

        with open(self.path, 'r') as f:
            contents = f.read()
        
        move_list = contents.split('"]\n\n').pop()

        with open(self.path, 'w', encoding='UTF-8') as f:
            f.write(f'{new_header}{move_list.strip(' +')}{'#' if self.result in ['1-0', '0-1'] else ''} {self.result}')
