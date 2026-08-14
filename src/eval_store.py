from multiprocessing.managers import SyncManager

class EvalStore():
    def __init__(self):
        self.positions = {}

        import threading
        self.lock = threading.Lock()

    def __repr__(self):
        p_dict = "{\n"
        for pos, eval in self.positions.items():
            p_dict += f'  -{pos}: {eval}\n'
        return p_dict + '}\n'

    def get_positions(self) -> dict[str, float]:
        return self.positions

    def set_positions(self, positions: dict[str, float]):
        self.positions = positions

    def update_evals(self, new_evals: dict[str, float]):
        self.positions |= new_evals

    def set_key(self, fen:str) -> str:
        # NOTE: position keys account only for piece positions,
        #       turn, and fifty move rule. They DO NOT account 
        #       for castling or en-passent possibilities.
        #       As of now, this is not an issue because position
        #       evaluations do not take ep or castling into account.
        parts = fen.split()
        fifty_mv = "T" if int(parts[-2]) >= 50 else "F"
        return f'{parts[0]}|{parts[1]}|{fifty_mv}'

    def parse_key(self, key:str) -> tuple[str,str,bool]:
        parts = key.split('|')
        draw_available = True if parts[2] == "T" else False
        return parts[0], parts[1], draw_available

    def get_eval(self, fen:str) -> tuple[float, bool]:
        key = self.set_key(fen)
        if key in self.positions:
            return self.positions[key], True
        return None, False

    def set_eval(self, fen:str, eval:float):
        key = self.set_key(fen)
        self.positions[key] = eval

    def get_locked_eval(self, fen:str) -> tuple[float, bool]:
        with self.lock:
            return self.get_eval(fen)

    def set_locked_eval(self, fen:str, eval:float):
        with self.lock:
            self.set_eval(fen, eval)


class EvalManager(SyncManager):
    ...