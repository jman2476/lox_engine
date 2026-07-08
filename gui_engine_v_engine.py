import pygame
from src.graphics.board import GUI_Board, Color, PromotionOptions
from src.graphics.clock import Clock
from src.graphics.error_box import ErrorBox
from src.graphics.button import ExitButton, SetFenButton
from src.graphics.mouse import get_square, move_notation, play_move
from src.engines.fool import FoolEngine
from src.engines.naive import NaiveEngine
from src.graphics.fen_box import FenBox
import datetime
import time
import logging
import sys

pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
running = True
dt = 0
elapsed = 0
last_move = 0
game_board = GUI_Board()
piece_font = pygame.font.Font("./fonts/nishiki-teki/NishikiTeki-MVxaJ.ttf", 30)
error_box = ErrorBox()

# Engine setup
engine_fool = FoolEngine(game_board.game, 'white')
engine_naive = NaiveEngine(game_board.game, 'black')

# Logging
# logger = logging.getLogger('find_moves')
# logging.basicConfig(filename='find_moves.log', level=logging.DEBUG)
# logger.info(f'Starting log {datetime.datetime.now()}')

# FenBox
fen_box = FenBox()
fen_button = SetFenButton(fen_box, game_board.game)
fen_box.set_text(game_board.game.fen)

if len(sys.argv) > 1:
    fen_box.set_text(sys.argv[1])
    fen_button.on_click()

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
 
    # Engine implementation
    if (game_board.game.winner is None and elapsed > 2.0 
        and elapsed - last_move > 2.0):
        if game_board.game.turn == 'white':
            engine_fool.pick_and_play_move()
            last_move = clock.tick(60)/1000
        elif game_board.game.turn == 'black':
            time.sleep(2)
            engine_naive.play_best_move()
            last_move = clock.tick(60)/1000
        
            
    screen.fill("purple")
    w_clock = Clock(datetime.timedelta(minutes=5), Color.WHITE)
    b_clock = Clock(datetime.timedelta(minutes=5), Color.BLACK)
    fen_box.set_text(game_board.game.fen)
    fen_box.render()
    
    w_clock.render()
    b_clock.render()

    screen.blit(w_clock, (900, 50))
    screen.blit(b_clock, (900, 140))
    screen.blit(error_box, (900, 230))
    screen.blit(exit_button, (1180, 0))
    
    # RENDER GAME HERE
    
    game_board.render_board(Color.WHITE, piece_font)
    
    
    screen.blit(game_board, (50, 50))
    # if move_piece is not None:
    #     screen.blit(move_piece, (move_piece.x_pos, move_piece.y_pos))
    screen.blit(piece_font.render("Hello, chess. Time: %.3f, Turn: %s"%(elapsed, game_board.game.turn), 0, "black"), (10,10))
    # screen.blit(piece_font.render("Fen: %s"%(game_board.game.fen), 0, "black"), (10,850))
    screen.blit(fen_box, (50, 855))
    screen.blit(fen_button, (950, 855))
    
    pygame.display.flip()

    dt = clock.tick(60)/1000
    elapsed += dt

pygame.quit()