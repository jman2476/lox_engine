import datetime, time, logging, sys
import pygame
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import matplotlib.pyplot as plt
import numpy as np
from src.graphics.board import GUI_Board, Color
from src.graphics.clock import Clock
from src.graphics.error_box import ErrorBox
from src.graphics.button import ExitButton, SetFenButton
from src.engines.fool import FoolEngine
from src.engines.naive import NaiveEngine
from src.graphics.fen_box import FenBox
from src.functions.game_writer import read_pgn

def main():
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
    engine_naive_b = NaiveEngine(game_board.game, 'black')
    # engine for white will use multprocessing
    engine_naive_w = NaiveEngine(game_board.game, 'white')
    game_board.game.b_player = 'Naive Single Proc'
    game_board.game.w_player = 'Naive Multi Proc'
    move_list = []
    ply_num = 0

    if len(sys.argv) > 2:
        pgn_file = sys.argv[2]
        pgn_dir = sys.argv[1]
        move_list, _ = read_pgn(pgn_file, pgn_dir)
    else:
        raise RuntimeError('gui_engine_replay requires a directory and pgn file to run')

    b_engine_d_t = []
    w_engine_d_t = []

    logger = logging.getLogger(__name__)

    # FenBox
    fen_box = FenBox()
    fen_button = SetFenButton(fen_box, game_board.game)
    fen_box.set_text(game_board.game.fen)

    # exit button
    exit_button = ExitButton()

    while running or ply_num < len(move_list):
        
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
                mv = engine_naive_w.play_move_mp_override(move_list[ply_num])
                end = time.perf_counter_ns()
                logger.info(f'white move {mv} took {end - start}s')
                w_engine_d_t.append(end - start)
                print(game_board.game.board)

            elif game_board.game.turn == 'black':
                start = time.perf_counter_ns()
                mv = engine_naive_b.play_move_override(move_list[ply_num])
                end = time.perf_counter_ns()
                logger.info(f'black move {mv} took {end - start}s')
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
        # screen.blit(piece_font.render("Fen: %s"%(game_board.game.fen), 0, "black"), (10,850))
        screen.blit(fen_box, (50, 855))
        screen.blit(fen_button, (950, 855))
        pygame.display.flip()

        dt = clock.tick(60)/1000
        elapsed += dt
        
        ply_num += 1
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
            # plt.axis((0, len(w_engine_d_t), min(b_engine_d_t), max(b_engine_d_t)))
            plt.minorticks_on()
            plt.suptitle(f'Naive Engine: Multi vs Single Process Move Time\nResult: {game_board.game.winner}\nFinal FEN: {game_board.game.fen}')
            print(f'Max time for black: {max(b_engine_d_t)}s')
            print(f'Min times: white {min(w_engine_d_t)}s, black {min(b_engine_d_t)}s')
            plt.show()
        
    pygame.quit()

if __name__ == '__main__':
    main()