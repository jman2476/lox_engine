import pygame
from src.graphics.board import GUI_Board, Color
from src.graphics.clock import Clock
from src.graphics.error_box import ErrorBox
from src.graphics.button import ExitButton, SetFenButton
from src.engines.fool import FoolEngine
from src.engines.naive import NaiveEngine
from src.graphics.fen_box import FenBox
import datetime
import time
import logging
import sys
import multiprocessing as mp
import matplotlib
matplotlib.use('QtAgg')
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import matplotlib.pyplot as plt
import numpy as np
from src.functions.save_game import save_game
from src.functions.depth_search import get_best_move

def main():
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

    # Depth search parameters
    depth = 3
    breadth = 5

    # Engine setup
    engine_naive_b = NaiveEngine(game_board.game, 'black', depth)
    # engine for white will use multprocessing
    engine_naive_w = NaiveEngine(game_board.game, 'white', depth)
    game_board.game.b_player = 'Naive Single Proc'
    game_board.game.w_player = 'Naive Single Proc'
    # game_board.game.w_player = 'Naive Multi Proc'

    b_engine_d_t = []
    w_engine_d_t = []

    # Logging
    logger = logging.getLogger(__name__)

    # FenBox
    fen_box = FenBox()
    fen_button = SetFenButton(fen_box, game_board.game)
    fen_box.set_text(game_board.game.fen)

    if len(sys.argv) > 1:
        fen_box.set_text(sys.argv[1])
        fen_button.on_click()

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
        if (game_board.game.winner is None and elapsed > 2.0):
            if game_board.game.turn == 'white':
                start = time.perf_counter_ns()
                get_best_move(engine_naive_w, depth, breadth, False)
                end = time.perf_counter_ns()
                w_engine_d_t.append(end - start)
                print(game_board.game.board)

            elif game_board.game.turn == 'black':
                start = time.perf_counter_ns()
                get_best_move(engine_naive_b, depth, breadth, False)
                end = time.perf_counter_ns()
                b_engine_d_t.append(end - start)
                print(game_board.game.board)
                
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
        screen.blit(fen_box, (50, 855))
        screen.blit(fen_button, (950, 855))
        pygame.display.flip()

        dt = clock.tick(60)/1000
        elapsed += dt
        
        if game_board.game.winner is not None:
            running = False
            w_x = range(1, len(w_engine_d_t) + 1)
            b_x = range(1, len(b_engine_d_t) + 1)
            plt.plot(w_x, w_engine_d_t, 'ro-', label="white")
            plt.plot(b_x, b_engine_d_t, 'bx-', label='black')
            plt.xlabel('move')
            plt.ylabel('elapsed time (ns)')
            plt.xticks(range(1,len(w_engine_d_t), 5))
            plt.autoscale(True, 'y')
            plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
            plt.minorticks_on()
            plt.suptitle(f'Naive Engine: Multi vs Single Process Move Time\nResult: {game_board.game.winner}\nFinal FEN: {game_board.game.fen}')
            print(f'Max time for black: {max(b_engine_d_t)}s')
            print(f'Min times: white {min(w_engine_d_t)}s, black {min(b_engine_d_t)}s')
            save_game(game_board.game.pgnw.path,
                      game_board.game.pgnw.title, 
                      plt.figure(num=1),
                      f'{game_board.game.w_player} v {game_board.game.b_player}-{game_board.game.pgnw.date}')
            plt.show()
    pygame.quit()

if __name__ == '__main__':
    mp.set_start_method('forkserver')
    main()