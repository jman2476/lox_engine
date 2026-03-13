from src.game import Game
import os, re

# write and read PGN files
def write_pgn(game, move=None, dir=None):
    pass

def read_pgn(pgn_file, dir=None):
    path = validate_path(pgn_file, dir)
    reg = r'\n(1\.[\s\S]*){1}'

    with open(path, 'r') as file:
       contents = file
   
    moves_block = re.match(reg, contents)
    moves_string = remove_newline(moves_block)
    moves = extract_moves(moves_string)


def validate_path(file_path, dir=None):
    path = file_path
    if dir is not None and os.path.exists(dir):
        path = os.path.join(dir, file_path)
    if not os.path.exists(path):
        raise Exception("Invalid path to PGN file")
    return path


def extract_moves(moves_string):
    split_moves = moves_string.split('.')
    moves = []
    for split in split_moves:
        if len(split) == 1: continue
        ply = split.split(' ')
        moves.append(ply[1], ply[2]) # ply[1] -> white ply, ply[2] -> black ply
    return moves

def remove_newline(moves_block):
    return ' '.join(moves_block.split('\n'))