from src.board import Board
from src.piece import (
    Piece, Pawn, King,
    Queen, Bishop,
    Knight, Rook
)
from src.game import Game
from src.functions.parse import parse_square
# from src.graphics.square import GUI_Square
import pygame
from enum import Flag, auto

class Color(Flag):
    WHITE = auto() 
    BLACK = auto()


class GUI_Board(pygame.Surface):
    _white = Color.WHITE
    _black = Color.BLACK
    _ranks = [i for i in range(0,8)]
    _files = list("abcdefgh")
 
    def __init__(self):
        pygame.Surface.__init__(self, (800, 800))
        self.game = Game()
        self.game.start_new_game()
        self.board = {
                "a":[None for i in range(0,8)],
                "b":[None for i in range(0,8)],
                "c":[None for i in range(0,8)],
                "d":[None for i in range(0,8)],
                "e":[None for i in range(0,8)],
                "f":[None for i in range(0,8)],
                "g":[None for i in range(0,8)],
                "h":[None for i in range(0,8)],
                }
        self.fill("green")
        self.set_squares()
        self.pieces = self.set_pieces()
        # self.render_board(Color.WHITE)

    def set_squares(self):
        color = self._white 
        for r in self._ranks:
            color = ~color
            for f in self._files:
                piece = self.game.board.board[f][r]
                # piece_icon = None if piece is None else piece.icon 
                self.board[f][r] = GUI_Square(color, f'{f}{r+1}', piece)
                color = ~color

    def set_pieces(self):
        return [GUI_Piece(p) for p in 
                [*self.game.board.white(), * self.game.board.black()]]
            
    def render_board(self, turn:Color, font:pygame.font.FontType):
        self.set_squares()
        self.pieces = self.set_pieces()
        def render_w_view():
            y = 700
            for r in self._ranks:
                x = 0
                for f in self._files:
                    self.blit(self.board[f][r], (x,y)) 
                    x += 100
                y -= 100
            for p in self.pieces:
                p.set_coords(turn)
                self.blit(p, (p.x_pos, p.y_pos))

        def render_b_view():
            y = 0
            for r in self._ranks:
                x = 700
                for f in self._files:
                    self.blit(self.board[f][r], (x,y))
                    x -= 100
                y += 100
            for p in self.pieces:
                p.set_coords(turn)
                self.blit(p, (p.x_pos, p.y_pos))

        match turn:
            case Color.WHITE:
                render_w_view()
            case Color.BLACK:
                render_b_view()

class GUI_Square(pygame.Surface):
    pygame.font.init()
    _font = pygame.font.SysFont("Arial", 20)

    def __init__(self, color:Color, square:str, piece:Piece):
        pygame.Surface.__init__(self, (100,100))
        self.color = color
        self.square = square
        self.__clear_sq__()
        self.piece = piece

    def __clear_sq__(self):
        self.fill(self.color.name)
        self.__render_sq_name__()

    def __render_sq_name__(self):
        self.blit(self._font.render(self.square, 0, 'grey'), (10,10))
    
class GUI_Piece(pygame.Surface):

    def __init__(self, piece:Piece):
        pygame.Surface.__init__(self, (100,100), flags=pygame.SRCALPHA)
        self.fill((0,0,0,0))
        self.piece = piece
        self.x_pos, self.y_pos = self.square_to_coordinates(Color.WHITE)
        
        self._set_icon()

    def square_to_coordinates(self, view:Color):
        file, rank = self.piece.file, self.piece.rank
        f_idx, r_idx = ord(file)-97, rank - 1

        def b_view():
            return 100 * (7-f_idx), 100 * r_idx
        
        def w_view():
            return 100 * f_idx, 100 * (7 - r_idx)
        
        if view == Color.WHITE:
            return w_view()
        else:
            return b_view()
    
    def _set_icon(self):
        path = f'./imgs/piece_icons/{self.piece.side}_{self.piece.name}.png'
        icon = pygame.image.load(path).convert_alpha()
        self.blit(icon, (0,0))
        print(f"Blitted {self.piece.name} for {self.piece.square()} at {self.x_pos},{self.y_pos}")

    def set_coords(self, view:Color):
        self.x_pos, self.y_pos = self.square_to_coordinates(view)