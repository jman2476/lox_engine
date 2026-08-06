import pygame

class GUIEvalBar(pygame.Surface):
    def __init__(self):
        super().__init__(self, (20, 100))
        self.eval:float = 0.0
        self.max:float = 30.0
        self.fill('white')
        self.font = pygame.freetype.Font("./fonts/kissinger2.ttf", 10)
        self.b_height = 50
        self.black_adv = pygame.Surface((20,self.b_height))

    def render(self):
        self.blit(self.black_adv, (0,0))

    def set_eval(self, eval:float):
        self.eval = eval
        # if abs(eval) > self.max:
        #     self.black_adv = pygame.Surface((20,100))
        # else:
        #     ...
        self.b_height -= eval
        self.black_adv = pygame.Surface((20, self.b_height))