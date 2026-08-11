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
                

## Depth multiprocessing