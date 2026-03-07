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
   


def validate_path(file_path, dir=None):
   path = file_path
   if dir is not None and os.path.exists(dir):
      path = os.path.join(dir, file_path)
   if not os.path.exists(path):
      raise Exception("Invalid path to PGN file")
   return path
