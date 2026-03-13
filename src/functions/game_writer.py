from src.game import Game
import os, re

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