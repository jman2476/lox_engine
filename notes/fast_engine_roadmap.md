# How does naive_engine work?
## No multiprocessing or depth
instantiate naive engine w/ game=> naive_
call naive_.play_best_move()
    -> calls self.rank_moves()
        -> calls self.evaluate_moves()
            -> takes self.find_moves() as arg
                returns results from find_move_notation
            - loops through moves
            - per mv, copy game and parse mv
            - if mv doesn't end game, call get_evaluation(game_copy.board)
            => return list[(move, eval)]
        - sort move list based on evaluation and turn
        => return best 10 moves
    - choose on available move at random
    => play chosen move, return move

## Move multiprocessing, depth single
instantiate naive engine w/ game=> naive_
call depth_search.get_best_move(naive_)
    -> calls depth_search()
        -> if moves == [], call get_ranked_moves()
            -> calls naive_.rank_moves_process()
                -> calls self.eval_moves_mp(self.find_moves())
                    -> creates Pool, each calls self.eval_move()
                        => returns (move, eval)
                    => return list of moves found
                - sort moves by eval and turn
                => return top 10 moves
            => returns the moves
        - for each now move, appends a depth chart of move to list
        - loop through moves
        - per mv, copy engine, parse mv on engine.game
        -> call get_ranked_moves() [see above]
        - set results from call to mv.next arr
        - call depth_search on mv.next
        => return moves
    - loop through moves in move_charts
    - crawl each move, look at last value on best path
    - if move has best found path, set as best_move
    - call engine.game.parse_move(best_move)

## Depth multiprocessing
instantiate naive engine w/ game => naive_
call depth_search.get_best_move_mp(naive_)
    -> call depth_search_multiprocess()
        -> calls get_ranked_moves() --> same as above
        - set Manager() as manager:
        - use manager to manage eval_dict
        - Pool w/ move args
        -> processes call search_process()
            - copy engine
            - parse mv on engine_copy.game
            - update e_copy.eval_dict w/ managed eval_dict
            -> call get_ranked_moves
                -> call engine.rank_moves()
                    -> call self.evaluate_moves(self.find_moves())
                        -checks by FEN if position has been seen, but it doesn't get matches because it includes castling and ep
                        => returns list[(move, eval)]
                    => sorts, returns best 10 moves
                => return move list
            -> calls depth_search() to continue
            -> update eval_dict w/ engine_copy.eval_dict
            => return move
        -> update engine.eval_dict w/ managed eval_dict
        => return depth chart move list
    -> as before, crawl depth charts, find best move
    => return best move
