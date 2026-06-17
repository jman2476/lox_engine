from src.board import Board
from src.piece import (
    Pawn, King,
    Queen, Bishop,
    Knight, Rook
)
from src.game import Game
# from src.graphics.square import GUI_Square
import pygame
from enum import Flag, auto

class Color(Flag):
    WHITE = auto() 
    BLACK = auto()


class GUI_Board(pygame.Surface):
    _white = Color.WHITE
    _black = Color.BLACK

    def __init__(self):
        pygame.Surface.__init__(self, (800, 800))
        self.game = Game()
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
        self.ranks = [i for i in range(0,8)]
        self.files = list("abcdefgh")
        self.fill("green")
        self.set_squares()
        self.render_board(Color.WHITE)

    def set_squares(self):
        color = self._white 
        for r in self.ranks:
            color = ~color
            for f in self.files:
                self.board[f][r] = GUI_Square(color, f'{f}{r+1}')
                color = ~color
            
    def render_board(self, turn:Color):
        if turn == Color.WHITE:
            self._render_w_view_() 
        else:
            self._render_b_view_()

    def _render_w_view_(self):
        y = 700
        for r in self.ranks:
            x = 0
            for f in self.files:
                self.blit(self.board[f][r], (x,y)) 
                x += 100
            y -= 100

    def _render_b_view_(self):
        y = 0
        for r in self.ranks:
            x = 700
            
            for f in self.files:
                self.blit(self.board[f][r], (x,y))
                x -= 100
            y += 100


class GUI_Square(pygame.Surface):
    pygame.font.init()
    _font = pygame.font.SysFont("Arial", 20)

    def __init__(self, color:Color, square:str):
        pygame.Surface.__init__(self, (100,100))
        self.color = color
        self.square = square   
        self.fill(self.color.name)
        self.__render_sq_name__()

    def __render_sq_name__(self):
        self.blit(self._font.render(self.square, 0, 'grey'), (10,10))