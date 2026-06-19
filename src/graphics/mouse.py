import pygame
from src.graphics.board import Color, GUI_Board

def get_square(turn:str, side_len:int, corner:tuple[int,int], mouse_pos:tuple[int,int]):
    board_pos = (mouse_pos[0] - corner[0] - 1, mouse_pos[1] - corner[1] - 1)
    file_idx, rank_idx = int(board_pos[0]/side_len), int(board_pos[1]/side_len)
    
    print(f'file: {file_idx}, row: {rank_idx}')
    if file_idx >= 8 or rank_idx >= 8:
        return None, None

    def get_sq_white():
        rank = GUI_Board._ranks[7-rank_idx]
        file = GUI_Board._files[file_idx]
        return file, rank + 1
    
    def get_sq_black():
        rank = GUI_Board._ranks[rank_idx] 
        file = GUI_Board._files[7-file_idx]
        return file, rank + 1
    
    match turn:
        case "white": print(get_sq_white())
        case "black": print(get_sq_black())
        
# def calc_dist()