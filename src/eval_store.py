import os
import shutil

class GrugEvalStore():
    def __init__(self, dir:str='./grug_eval'):
        self.path = self.set_path(dir)

    def set_path(self, dir:str) -> str:
        abs_path = os.path.abspath(dir)
        if os.path.exists(abs_path):
            shutil.rmtree(abs_path)
        os.mkdir(abs_path)
        return abs_path

    def store_eval(self, fen:str, eval:float) -> tuple[str,str,float]:
        ...

    def create_file_name(self, fen:str, eval:float) -> str:
        board_state = '_'.join(fen.split()[:2])
        return f'{board_state}={eval:.2f}.txt'

    def parse_file_name(self, file:str) -> tuple[str,str,float]:
        ...

    def find_and_set_eval(self, fen:str, eval:float) -> tuple[str,str,float]:
        ...