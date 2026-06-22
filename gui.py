import pygame
from src.graphics.board import GUI_Board, Color
from src.graphics.clock import Clock
from src.graphics.mouse import get_square
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

# mouse handlers
dragging = False
move_piece = None

# test game => automation
move_list = ["e4", "d5", "Ke2", "Kd7", "Qe1", "Qe8", "Kd1", "Kd8"]
move_idx = 0
trigger = 5 #seconds
mouse_msgs = []

# dnd test vars
# circle_pos = pygame.Vector2(1000, 450)

while running:
    sigma_offset = (0,0)
    offset = (0,0)
    # drag_v = pygame.Vector2()
    events = pygame.event.get()
    # print(f'Events {events}') 
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # dist = circle_pos.distance_to(pygame.Vector2(event.pos))
            # if dist <=40:
            #     dragging = True
            init_sq = get_square(game_board.game.turn, 100, (50,50), pygame.mouse.get_pos())
            if init_sq != (None, None):
                move_piece = game_board.board[init_sq[0]][init_sq[1]-1][1]
            
            print(f'init_sq {init_sq}, move_piece {move_piece}')
            if move_piece is not None:
                dragging = True
            square = get_square(game_board.game.turn, 100, (50,50), pygame.mouse.get_pos())
            # if square is not None and square[0] is not None and square[1] is not None:
                # move_piece = game_board.board[square[0]][square[1]-1][1]
                # if move_piece is not None:
                    # print(f'{move_piece.piece.side} {move_piece.piece.name}')
            mouse_msgs.append(f'Start: Mouse {"is" if dragging else "isn't"} dragging from {event.pos}. Square start: {square}')
        if event.type == pygame.MOUSEMOTION and dragging == True:
            if move_piece:
                move_piece.set_drag_coords(pygame.mouse.get_pos())
                print(f'mouse position: {move_piece.x_pos}, {move_piece.y_pos}')
            # offset = pygame.mouse.get_rel()
            # circle_pos = pygame.Vector2(pygame.mouse.get_pos())
            # sigma_offset = (sigma_offset[0]+offset[0], sigma_offset[1]+offset[1])
            # mouse_msgs.append(f'Middle: Moving mouse, offset: {offset}, sigma_offset: {sigma_offset}')
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            fin_sq = get_square(game_board.game.turn,100, (50,50), pygame.mouse.get_pos())
            mouse_msgs.append(f'End: Mouse {"is" if dragging else "isn't"} dragging to {event.pos}. Square end: {fin_sq}')
            sigma_offset = (0,0)
            
    if len(mouse_msgs) > 0:
        print("Mouse messages:", mouse_msgs)
    mouse_msgs = []
    screen.fill("purple")
    w_clock = Clock(datetime.timedelta(minutes=5), Color.WHITE)
    b_clock = Clock(datetime.timedelta(minutes=5), Color.BLACK)
    
    w_clock.render()
    b_clock.render()

    screen.blit(w_clock, (1000, 500))
    screen.blit(b_clock, (1000, 600))
    

    # MOUSE OBSERVATION
    # mouse = pygame.mouse.get_pos() 
    # print(f'Buttons {pygame.mouse.get_pressed()}') 
    # print(f'Get focused {pygame.mouse.get_focused()}') 
    # print(f'Get pos {mouse}') 
    # print(f'Get rel pos {pygame.mouse.get_rel()}') 
    

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
    if move_piece is not None:
        screen.blit(move_piece, (move_piece.x_pos, move_piece.y_pos))
    screen.blit(piece_font.render("Hello, chess. Time: %.3f, Turn: %s"%(elapsed, game_board.game.turn), 0, "black"), (10,10))
    screen.blit(piece_font.render("Fen: %s"%(game_board.game.fen), 0, "black"), (10,850))
    
    # drag n drop test
    # pygame.draw.circle(screen, 'red',circle_pos, 40)
    pygame.display.flip()

    dt = clock.tick(60)/1000
    elapsed += dt

pygame.quit()