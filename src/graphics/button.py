import pygame


class Button(pygame.Surface):
    def __init__(self, size:tuple[int,int]):
        pygame.Surface.__init__(self, size)
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