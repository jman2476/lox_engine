import pygame


class FenBox(pygame.Surface):

    def __init__(self):
        pygame.Surface.__init__(self, (900, 40))
        self.fill('lightpink')
        self.text = 'potatos'
        self.font = pygame.freetype.Font("./fonts/kissinger2.ttf", 25)
        # self.font = pygame.freetype.SysFont('Arial', 20)

    def render(self):
        self.fill('lightpink')
        self.font.render_to(self, (2,7), self.text, 'orchid')

    def set_text(self, text:str):
        self.text = text