from src.functions.parse import parse_square

def get_horizontal_squares(left:str, right:str): # left -> a, right -> h
    if left[1] != right[1]:
        raise ValueError(f'Squares {left} and {right} are not horizontally aligned')
    files = list("abcdefgh") 
    rank = left[1]
    init, fin = [files.index(sq[0]) for sq in [left, right]]
    return [f'{files[f]}{rank}' for f in range(init, fin + 1)]

def get_vertical_squares(bottom:str, top:str): # bottom -> 1, top -> 8
    if bottom[0] != top[0]:
        raise ValueError(f'Squares {bottom} and {top} are not vertically aligned')
    file, edges = bottom[0], (int(bottom[1]), int(top[1]))
    return [f'{file}{r}' for r in range(edges[0], edges[1] + 1)]
    