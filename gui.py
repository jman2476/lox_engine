import pygame
from src.graphics.board import GUI_Board
# based on quick start from pygame.org/docs

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True
dt = 0
game_board = GUI_Board()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    
    # RENDER GAME HERE
    screen.blit(game_board, (50, 50))
    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]: 
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60)/1000

pygame.quit()