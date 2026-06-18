import pygame
import datetime
from src.graphics.board import Color


class Clock(pygame.Surface):
    pygame.font.init()
    _font = pygame.font.SysFont("Arial", 30)

    def __init__(self, start_time:datetime.timedelta, side:Color):
        pygame.Surface.__init__(self, (160, 80))
        self.color = side
        self.fill(self.color.name)
        self.remaining = start_time
        
    def render(self):
        opp_color = ~self.color
        self.blit(self._font.render(f"{self.remaining}", 0, opp_color.name), (10,10))