import pygame
from src.graphics.board import GUI_Board, Color
from src.graphics.clock import Clock
from src.graphics.square import get_square
import datetime
# based on quick start from pygame.org/docs

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True
dt = 0
elapsed = 0
game_board = GUI_Board()
piece_font = pygame.font.Font("./fonts/nishiki-teki/NishikiTeki-MVxaJ.ttf", 30)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)

# test game => automation
move_list = ["e4", "d5", "Ke2", "Kd7", "Qe1", "Qe8", "Kd1", "Kd8"]
move_idx = 0
trigger = 5 #seconds

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    w_clock = Clock(datetime.timedelta(minutes=5), Color.WHITE)
    b_clock = Clock(datetime.timedelta(minutes=5), Color.BLACK)
    
    w_clock.render()
    b_clock.render()

    screen.blit(w_clock, (1000, 500))
    screen.blit(b_clock, (1000, 600))
    

    # MOUSE OBSERVATION
    mouse = pygame.mouse.get_pos()
    print(f'Buttons {pygame.mouse.get_pressed()}')
    print(f'Get focused {pygame.mouse.get_focused()}')
    print(f'Get pos {mouse}')
    print(f'Get rel pos {pygame.mouse.get_rel()}')
    get_square(game_board.game.turn, 100, (50,50), mouse)

    # AUTO PLAY GAME HERE
    
    if elapsed > trigger:
        if not move_idx >= len(move_list):
            game_board.game.parse_move(move_list[move_idx])
            move_idx += 1
            trigger += 10
        # else:
        #     break
    
    # RENDER GAME HERE
    match(game_board.game.turn):
        case "white":
            game_board.render_board(Color.WHITE, piece_font)
        case "black":
            game_board.render_board(Color.BLACK, piece_font)
    screen.blit(game_board, (50, 50))
    screen.blit(piece_font.render("Hello, chess. Time: %.3f, Turn: %s"%(elapsed, game_board.game.turn), 0, "black"), (10,10))
    screen.blit(piece_font.render("Fen: %s"%(game_board.game.fen), 0, "black"), (10,850))

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
    elapsed += dt

pygame.quit()