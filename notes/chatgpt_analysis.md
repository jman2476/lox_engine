
My strongest recommendation is to establish reliable rules and search correctness before investing further in multiprocessing. I found several concrete issues that can affect the engine’s decisions, alongside useful foundations: separate move-generation and attack-map logic, FEN support, multiple engine implementations, and tests.
I reviewed commit c8d443f, dated September 13. This was a static source review: I did not execute the engine or tests, write code, or make changes. The examples below are cases for him to investigate.

The search-tree evaluator does not consistently implement minimax.
In depth_search.py, lines 110–136, the choice between minimum and maximum can depend on the side associated with a deeper leaf. It needs to depend on whose decision is being evaluated at the current branch.

For example, suppose Black has two replies. After White chooses its best continuation, those replies yield scores of \(+9\) and \(-4\), measured from White’s perspective. Black chooses \(-4\). The current traversal can instead select \(+9\), because the deeper moves were White’s.

This can make the engine assume favorable cooperation from its opponent. Both search implementations use this traversal.

Suggested exercise: test the traversal on tiny artificial trees with known numerical answers, independently of chess. Include different depths and branches that terminate early. This isolates the search algorithm from move-generation and evaluation errors.

Concurrent workers can silently lose branches of the search tree.
In fast_depth_search.py, lines 275–280, workers read a parent and append a child before acquiring the lock; only the final assignment is protected.

Two workers can therefore read the same parent, append different children to their separate copies, and overwrite each other’s results. The final tree then omits a branch that was actually searched.

The operation that needs protection is the complete read → modify → write sequence. Interestingly, the alternative search_proc_4 implementation already groups these operations under one lock, but the active worker is search_process.

There is also a failure-handling issue: an exception during a task can prevent its completion acknowledgment, leaving the parent waiting indefinitely at the queue’s join. Failed work needs to reach the parent as an explicit failure. See the worker body.

Two draw rules need correction.
Location	Finding
game.py, lines 280–284	The fifty-move rule triggers at 50 half-moves. Fifty moves by each player corresponds to 100 half-moves.
game.py, lines 82–89	Repetition compares only piece placement. It must also distinguish the side to move, castling rights, and legally available en-passant captures.
These requirements follow from FIDE Articles 9.2–9.3. Using the entire FEN unchanged would introduce another problem: its move counters should not distinguish repeated positions.
He should also decide explicitly whether the application automatically claims available draws. Official rules distinguish claimable threefold/fifty-move draws from automatic fivefold/seventy-five-move draws.

The existing fifty-move test expects the incorrect threshold, so the test and implementation currently reinforce the same misunderstanding.

The evaluation cache mixes values that require different information.
EvalStore’s key deliberately omits castling and en-passant information. That can be defensible for a purely static evaluator that ignores those features.

However, FastEngine.eval_moves also caches checkmate and draw results—and accepts a cache hit before considering the newly calculated game result.

Consequently, a position reached for the third time can reuse a nonzero evaluation from an earlier occurrence. Conversely, a repetition draw can store zero for another occurrence that is not drawn.

Suggested principle: every cached value must be determined by the information in its key. Keep history-dependent adjudication separate from static position evaluation. A full FEN alone does not contain repetition history.

Castling legality differs between move generation and move execution.
find_king_moves checks the transit and destination squares for castling, but does not check whether the king is currently in check.

The castling parser does reject castling out of check. Those two components therefore disagree.

This matters beyond generating an invalid candidate: checkmate detection relies on the generated move list being legal. A spurious castle can make that list nonempty and conceal checkmate.

A useful invariant is: every move returned by the legal move generator must execute successfully and leave its own king safe.

Promotion parsing bypasses essential pawn validation.
In parse.py, lines 134–153, promotion captures directly replace pieces. They do not verify that the starting pawn belongs to the moving player or that the destination is on an adjacent file.

A concrete case to try is this FEN:

7r/P6k/8/8/8/8/8/4K3 w - - 0 1

Then attempt axh8=Q. That asks the pawn on a7 to capture across the board onto h8. Tracing the promotion branch indicates that it accepts the move.

Suggested exercise: make promotion satisfy the same movement and ownership rules as an ordinary pawn move, with promotion as an additional consequence.

The test suite needs stronger guarantees about what “passing” means.
There are several specific opportunities:

test_fast_depth_search.py, lines 2–5 imports depth_search_tree, whose definition is commented out. That is an import-time blocker for this test module.
Much of test_find_moves.py prints results without asserting the expected moves. Its first test also catches exceptions without failing.
test_game_end_conditions.py defines test_fifty_move_from_start twice. Python retains only the second definition.
test_fastengine.py, lines 25–59 checks evaluations only for moves that were returned. An empty result can pass those loops.
Checking the complete expected result, including missing moves, would make these tests much more informative.
The search strategy itself deserves a separate decision. FastEngine retains only the best-looking moves according to their immediate evaluations, then searches those further. This is a form of beam search: a sacrifice or quiet defensive move can be discarded before its value becomes visible. Increasing depth cannot recover a move already discarded. There is also a hard limit of ten moves before the configured breadth is applied.
For learning, I would suggest first establishing ordinary minimax over all legal moves at modest depths, then adding alpha–beta pruning and checking that it preserves the answer for the same search tree. Quiescence search—continuing tactically unstable positions beyond the normal cutoff—is a useful subsequent exercise.

I would also qualify the diagnosis in why_is_fds_so_slow.md:

The active implementation performs local evaluation lookups, but transfers whole caches between processes per task. The bulk copying and synchronization in fast_depth_search.py deserve measurement.
The checked-in profile does not establish that waiting time is all communication overhead. It records about 4.7 seconds in join, while the profiler is enabled in the parent process. That includes waiting for workers to compute. Worker profiles are needed to distinguish computation, copying, serialization, and synchronization. See the profiling setup and recorded output.
The shallow-copy suggestion does not fit the current board representation. Board contains mutable lists and mutable pieces. A shallow dictionary copy would share those objects across hypothetical positions.
The architectural change I would encourage him to explore is a small, explicit position-and-move model. Search currently generates notation, reparses it, copies a Game containing PGN machinery, and performs further move generation during adjudication. An internal move represented by its starting square, destination, and promotion choice would make the rules easier to test and reduce repeated parsing. A position object could hold the state needed for rules and search, while the game interface handles notation, files, clocks, and display.
For his next learning milestones, I would choose:

Exact move-generation tests and perft. Perft counts legal move sequences to a specified depth. It tests the rules without involving evaluation or move selection; Stockfish’s tests demonstrate this approach. Include positions exercising castling, en passant, pins, checks, and underpromotion.
Independent comparisons. Compare legal moves against python-chess across fixed positions. His implementation remains his own; the second implementation supplies an independent check.
Search invariants. Verify known minimax answers, unchanged input positions after search, agreement with caching enabled or disabled, and equivalent results across worker counts.
Controlled performance experiments. Use the same positions, search settings, and cache conditions over repeated runs. Keep timing experiments separate from correctness tests—the current assertion that one cached run must be faster can fail simply because of scheduling noise