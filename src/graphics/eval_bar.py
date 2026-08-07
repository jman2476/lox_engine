import pygame

class EvalBar(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, (30, 800))
        self.eval:float = 0.0
        self.max:float = 30.0
        self.fill('white')
        self.font = pygame.freetype.Font("./fonts/kissinger2.ttf", 10)
        self.b_height = 400
        self.black_adv = pygame.Surface((30,self.b_height))

    def render(self):
        self.fill('white')
        self.blit(self.black_adv, (0,0))

    def set_eval(self, eval:float):
        if eval != self.eval:
            print(f'Evaluation: {self.eval}')
        self.eval = eval
        self.b_height = 400 - (self.eval*20)
        if self.b_height < 0: self.b_height = 0.0
        if self.b_height > 800.0: self.b_height = 800.0
        self.black_adv = pygame.Surface((30, self.b_height))