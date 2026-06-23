import pygame
from src.game import Game
from src.piece import (
    Piece, Pawn, King,
    Queen, Bishop,
    Knight, Rook
)
from src.graphics.board import Color, GUI_Board

class MoveTranslator():
    pass

   

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
        case "white": return get_sq_white()
        case "black": return get_sq_black()
        
def play_move(game:Game, piece:Piece, i_sqr:tuple[str, int], f_sqr:tuple[str, int]):
    capture, _, __ = game.board.check_square_filled(f_sqr[0], f_sqr[1])
    move_sq = f'{f_sqr[0]}{f_sqr[1]}'
    piece_notation = {
        'king': 'K',
        'queen': 'Q',
        'bishop': 'B',
        'knight': 'N',
        'rook': 'R'
    }
    

    def pawn_move():
        print("---Pawn Debugging---")
        print(f'Init sq: {i_sqr[0]}{i_sqr[1]}')
        print(f'Fin_sq: {f_sqr[0]}{f_sqr[1]}')
        print(f'Pawn sq: {piece.square()}')
        print('--------------------')
        ep = game.en_passent == f'{f_sqr[0]}{f_sqr[1]}'
        if piece.move_valid(f_sqr[1], f_sqr[0], game.board, ep):
            return f'{i_sqr[0] + "x" if capture or ep else ''}'
        return None
    
    def king_move():
        if piece.move_valid(f_sqr[1], f_sqr[0], game.board):
            return f'K{'x' if capture else ''}'
        return None
    
    def piece_move():
        if piece.move_valid(f_sqr[1], f_sqr[0], game.board):
            char = piece_notation[piece.name]
            init_sqr = f'{i_sqr[0]}{i_sqr[1]}'
            return f'{char}{init_sqr}{'x' if capture else ''}'
        return None
    
    match piece.name:
        case 'pawn':
            mv = pawn_move()
            if mv is not None: return mv + move_sq
            return mv
        case 'king':
            mv = king_move()
            if mv is not None: return mv + move_sq
            return mv
        case _:
            mv = piece_move()
            if mv is not None: return mv + move_sq
            return mv