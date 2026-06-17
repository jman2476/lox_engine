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

    def set_squares(self):
        color = self._white 
        x, y = 0, 0
        for r in self.ranks:
            x = 0
            color = ~color
            for f in self.files:
                print(f'light: {color.name}, (x,y): ({x},{y})')
                square = self.board[f][r]
                square = GUI_Square(color, x, y)
                x += 100
                color = ~color
                self.blit(square, (square.x_pos, square.y_pos))
            y += 100
            
    def render_board(self, turn:Color):
        if turn == Color.WHITE:
            self.__render_w_view__() 
        else:
            self.__render_b_view__()

    def _render_w_view_(self):
        pass

    def _render_b_view_(self):
        pass


class GUI_Square(pygame.Surface):
    def __init__(self, color:Color, x:int = 0, y:int = 0):
        pygame.Surface.__init__(self, (100,100))
        self.color = color
        (self.x_pos, self.y_pos) = (x, y)
        self.fill(self.color.name)

    def set_position(self, x:int, y:int):
       self.x = x
       self.y = y