import os
import shutil
from multiprocessing.managers import BaseManager

# Depricated: GrugEvalStore lookups would be O(n) to find pre-evaluated positions
#               Actually implementing this would massively drive down performance,
#               and negate any actual benefit from caching values
#       However: I can use the methods here for implementing a proper eval store


class GrugEvalStore():
    def __init__(self, dir:str='./grug_eval'):
        self.path = self.set_path(dir)


    def set_path(self, dir:str) -> str:
        abs_path = os.path.abspath(dir)
        if os.path.exists(abs_path):
            shutil.rmtree(abs_path)
        os.mkdir(abs_path)
        print(f'\ngrug using path {abs_path}\n')
        return abs_path

    def get_path(self):
        return self.path

    def store_eval(self, fen:str, eval:float) -> tuple[str,str,float]:
        file = self.create_file_name(fen, eval)
        file_path = os.path.join(self.path, file)
        try:
            with open(file_path, 'x') as f:
                f.write(f'{file_path}')
        except Exception as e:
            print(f'Exception storing eval {file}: {e}')
        finally:
            return self.parse_file_name(file)

    def create_file_name(self, fen:str, eval:float) -> str:
        clean_fen = '='.join(fen.split('/'))
        board_state = '_'.join(clean_fen.split()[:2])
        return f'"{board_state}_{eval:.2f}".txt'

    def parse_file_name(self, file:str) -> tuple[str,str,float]:
        parts = file.strip('".txt').split('_')
        fen = '/'.join(parts[0].split('='))
        eval = parts[2]
        return fen, parts[1], float(eval)

    def find_set_eval(self, fen:str, eval:float) -> tuple[str,str,float]:
        ...

class GrugManager(BaseManager):
    ...