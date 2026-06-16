import pygame

# based on quick start from pygame.org/docs

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()