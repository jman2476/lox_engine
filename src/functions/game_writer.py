from src.game import Game
import os, re
import datetime as dt

# write and read PGN files
def write_pgn(game, move=None, dir=None):
    pass

def read_pgn(pgn_file, dir=None):
    path = validate_path(pgn_file, dir)
    # print(f'pgn file path: {path}\n')
    regex = r'\n(1\.[\s\S]*){1}'

    with open(path, 'r') as file:
       contents = file.read()
    # print(f"file contents: {contents}")
    moves_block = re.search(regex, contents, re.MULTILINE)
    # print(f'moves block \n {moves_block}\n {moves_block.group(0)}')
    moves_string = remove_newline(moves_block.group(0))
    moves = extract_moves(moves_string)
    result = moves[-1][-1]
    print(result)

    return moves, result


def validate_path(file_path, dir='.'):
    path = file_path
    absolute_dir = os.path.abspath(dir)
    if dir is not None and os.path.exists(dir):
        path = os.path.join(absolute_dir, file_path)
    if not os.path.exists(path):
        raise Exception("Invalid path to PGN file")
    return path


def extract_moves(moves_string):
    split_moves = moves_string.split('.')
    moves = []
    for split in split_moves:
        # print(f'Move "{split}"')
        if len(split) <= 2: continue
        ply = split.split(' ')
        moves.append([ply[1], ply[2]]) # ply[1] -> white ply, ply[2] -> black ply
        if len(ply) == 4 and '-' in ply[3]:
            moves.append([ply[3]])
    return moves

def remove_newline(moves_block):
    return ' '.join(moves_block.split('\n'))

class PGNWriter():
    def __init__(self, game, dir:str='./recent_games'):
        self.event = ''
        self.site = 'Lox Engine'
        self.date = dt.date.today()
        self.round = '1'
        self.white = game.w_player
        self.black = game.b_player
        self.result = game.winner
        self.title = f'{self.white} v {self.black}-{self.date}.pgn'
        self.path = os.path.join(self.set_path(dir), self.title)

    def create_file(self):

        with open(self.path, 'w', encoding='UTF-8') as file:
            ...

    def set_path(self, dir:str):
        abs_dir_path = os.path.abspath(dir)
        if not os.path.exists(abs_dir_path):
            os.mkdir(abs_dir_path)
        return abs_dir_path
    
    def format_header(self):
        return f'''[Event "{self.event}"]
        [Site "{self.site}"]
        [Date "{self.date}"]
        [Round "{self.round}"]
        [White "{self.white}"]
        [Black "{self.black}"]
        [Result "{self.result}"]

        
        '''