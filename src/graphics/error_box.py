import pygame

class ErrorBox(pygame.Surface):
    pygame.font.init()
    _font = pygame.font.SysFont("Arial", 20)
    def __init__(self):
        pygame.Surface.__init__(self, (300, 400))
        self.fill('black')
        self.message = ''
        
    def set_message(self, message:str):
        self.message = message
        # self.__render__()
        self.__render_text__()
        
    def __render__(self):
        self.blit(self._font.render(self.message, 0, 'cornsilk'), (0,0))
        
    def __render_text__(self):
        # surface == self
        rect = self.get_rect()
        y = rect.top
        spacing = -2
        font_height = self._font.size("Tj")[1]
        text = self.message        
        
        while text:
            i = 1

            if y + font_height > rect.bottom: break

            while self._font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            
            if i < len(text):
                i = text.rfind(" ", 0,i) + 1
                
            self.blit(self._font.render(text[:i], 0, 'cornsilk'), (rect.left, y))
            y += font_height + spacing
            
            text = text[i:]
            
        return text

