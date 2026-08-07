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