import pygame
from src.graphics.board import GUI_Board, Color, PromotionOptions
from src.graphics.clock import Clock
from src.graphics.error_box import ErrorBox
from src.graphics.button import ExitButton
from src.graphics.mouse import get_square, move_notation, play_move
import datetime

pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True
dt = 0
elapsed = 0
game_board = GUI_Board()
piece_font = pygame.font.Font("./fonts/nishiki-teki/NishikiTeki-MVxaJ.ttf", 30)
error_box = ErrorBox()

# mouse handlers
dragging = False
move_piece = None
init_tracker = None

# test game => automation
move_list = ["e4", "d5", "Ke2", "Kd7", "Qe1", "Qe8", "Kd1", "Kd8"]
move_idx = 0
trigger = 5 #seconds
mouse_msgs = []

# exit button
exit_button = ExitButton()

while running:
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > 1180 and mouse_pos[1] < 20:
                exit_button.on_click()

            if game_board.promoting['current']:
                if mouse_pos[0] > 50 and mouse_pos[0] < 150:
                    p = ''
                    if mouse_pos[1] > 50 and mouse_pos[1] < 150:
                        p = game_board.promoting['options'].buttons[0].on_click(game_board)
                        print(f"Promotion to {p}")
                    elif mouse_pos[1] > 150 and mouse_pos[1] < 250:
                        p = game_board.promoting['options'].buttons[1].on_click(game_board)
                        print(f"Promotion to {p}")
                    elif mouse_pos[1] > 250 and mouse_pos[1] < 350:
                        p = game_board.promoting['options'].buttons[2].on_click(game_board)
                        print(f"Promotion to {p}")
                    elif mouse_pos[1] > 350 and mouse_pos[1] < 450:
                        p = game_board.promoting['options'].buttons[3].on_click(game_board)
                        print(f"Promotion to {p}")
                    game_board.promoting['new'] = p
            else:        
                init_sq = get_square(game_board.game.turn, 100, (50,50), mouse_pos)
                if init_sq != (None, None):
                    move_piece = game_board.clear_square(init_sq)
                    init_tracker = init_sq
                
                print(f'init_sq {init_sq}, move_piece {move_piece}')
                if move_piece is not None:
                    dragging = True
                    move_piece.set_drag_coords(mouse_pos)
                square = get_square(game_board.game.turn, 100, (50,50), mouse_pos)

        # Mouse drag
        if event.type == pygame.MOUSEMOTION and dragging == True:
            if move_piece:
                move_piece.set_drag_coords(pygame.mouse.get_pos())

        # Mouse up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            fin_sq = get_square(game_board.game.turn,100, (50,50), pygame.mouse.get_pos())

            if game_board.promoting['current'] and game_board.promoting['new'] != '':
                print("about to execute promotion")
                move, err = move_notation(*(game_board.promoting['move']))
                if err is not None:
                    print("Error writing move notation ", move, err)
                    error_box.set_message(str(err))
                elif move is not None:
                    print(f"Algebraic notation: {move}")
                    error_box.set_message(str(play_move(game_board.game, move)))
                    print("-------------------------")
                    print(f'FEN: {game_board.game.fen}')
                    print("-------------------------")
            elif fin_sq[0] is not None and move_piece is not None:
                move, err = move_notation(game_board, move_piece.piece, init_tracker, fin_sq)
                if err is not None:
                    print("Error writing move notation ", move, err)
                    error_box.set_message(str(err))
                elif move is not None and not game_board.promoting['current']:
                    print(f"Algebraic notation: {move}")
                    error_box.set_message(str(play_move(game_board.game, move)))
                    print("-------------------------")
                    print(f'FEN: {game_board.game.fen}')
                    print("-------------------------")
            else:
                error_box.set_message("Don't throw pieces off the board")
            
            if not game_board.promoting['current']:
                init_tracker = None
                if move_piece:
                    move_piece.set_drag_coords((-100, -100))
                game_board.drag_square = (None, None)
                move_piece = None
            
    if len(mouse_msgs) > 0:
        print("Mouse messages:", mouse_msgs)
    mouse_msgs = []
    screen.fill("purple")
    w_clock = Clock(datetime.timedelta(minutes=5), Color.WHITE)
    b_clock = Clock(datetime.timedelta(minutes=5), Color.BLACK)
    
    
    w_clock.render()
    b_clock.render()

    screen.blit(w_clock, (900, 50))
    screen.blit(b_clock, (900, 140))
    screen.blit(error_box, (900, 230))
    screen.blit(exit_button, (1180, 0))
    
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
    
    pygame.display.flip()

    dt = clock.tick(60)/1000
    elapsed += dt

pygame.quit()