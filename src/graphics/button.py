import pygame
from src.graphics.fen_box import FenBox
# from src.graphics.board import GUI_Board
# from src.graphics.color import Color
from src.game import Game


class Button(pygame.Surface):
    def __init__(self, size:tuple[int,int], flags:int = 0):
        pygame.Surface.__init__(self, size, flags=flags)
        self.font = pygame.freetype.Font("./fonts/kissinger2.ttf", 20)
        
    def on_click(self):
        # must override
        pass
    

class ExitButton(Button):
    def __init__(self):
        super().__init__((20,20))
        self.fill('red')
        self.font.render_to(self, (5,2), 'x', 'white', 'red', size=25)

    def on_click(self):
        pygame.quit()

class SetFenButton(Button):
    def __init__(self, fenbox:FenBox, game:Game):
        super().__init__((100,40))
        self.fill('fuchsia')
        self.font.render_to(self, (5,10), 'Set FEN', 'lavender', 'fuchsia', size=25)
        self.fenbox = fenbox
        self.game = game

    def on_click(self):
        self.game.read_fen(self.fenbox.text)
        self.game.set_fen()
