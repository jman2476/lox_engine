# A place for thoughts while debugging

## gui_engine_v_engine.py not printing final checkmate move in some situations
## FEN: 6R1/8/2B5/4Q3/P1k2P1P/8/3K4/8 w - - 3 34
last move and board position registered in terminal and gui is by black king, but terminal shows that black is checkmated, and it is white's turn. In the position, white is one move from checkmating black, so it seems like the move was played, but it was not registered in the terminal or the gui before the game loop exited.
