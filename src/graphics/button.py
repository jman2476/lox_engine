import pygame
from src.graphics.board import Color


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

class PromotionOptions(pygame.Surface):
    _pieces = [
        'queen',
        'rook',
        'bishop',
        'knight'
    ]

    def __init__(self, side:Color):
        pygame.Surface.__init__(self,(100,400))
        self.fill('beige')
        self.side = side
        
    def __set_buttons__(self):
        for i, piece in enumerate(self._pieces):
            pos = (i*100, 0)
            button = PromotionButton(piece, self.side)
            self.blit(button, pos)

class PromotionButton(Button):
    def __init__(self, piece:str, side: Color):
        super().__init__((100,100), pygame.SRCALPHA)
        self.side = side
        self.piece = piece
        self.icon = self.__set_icon__()
        self.blit(self.icon, (0,0))

    def __set_icon__(self):
        path = f'./imgs/piece_icons/{self.side}_{self.piece}' 
        return pygame.image.load(path).convert_alpha()
    
    def on_click(self):
        return self.piece[:1].capitalize()