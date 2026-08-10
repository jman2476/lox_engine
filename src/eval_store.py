from multiprocessing.managers import BaseManager

class EvalStore():
    def __init__(self, lock):
        self.positions = {}
        self.lock = lock


    def set_key(self, fen:str) -> str:
        parts = fen.split()
        fifty_mv = "T" if int(parts[-2]) >= 50 else "F"
        return f'{parts[0]}|{parts[1]}|{fifty_mv}'

    def parse_key(self, key:str) -> tuple[str,str,bool]:
        parts = key.split('|')
        draw_available = True if parts[2] == "T" else False
        return parts[0], parts[1], draw_available

class EvalManager(BaseManager):
    ...