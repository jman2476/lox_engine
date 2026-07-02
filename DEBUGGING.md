# A place for thoughts while debugging

## is_checkmated race condition
So far, a checkmated side shows multiple valid moves if their king is checkmated and they have pieces that would otherwise move. 
This goes away when a breakpoint is set in the is_checkmated function at the line `move_lists = [find_available_moves(game_copy, p) for p in pieces]` or the lines where `gm = copy.deepcopy(game)` is called in find_moves.py.
In addition to breakpoints, this works with logging before those lines.
When logging from within the find_available_moves function, the behavior is removed if logging happens before the `match case` statement, and only the first piece's invalid moves are registered if logging happens after the `match case` statement.

Oddly, the behavior is removed for all pieces if logging happens in the first line of find_pawn_moves(), even non-pawn pieces do not register their invalid moves (assuming they would have them).
Current method to finding the origin of the race condition is to move the logging statement down through the find_pawn_moves function, and see what is the highest line it can be placed while still showing the error.

Tried so far: (safe/unsafe)
1. start of function -> safe
2. end/just before return -> unsafe
3. before valid_moves loop -> safe
4. before all_valid loop -> unsafe
5. valid_moves except block -> unsafe
6. above if gm.fen!=game.fen -> safe
7. under fen check conditional block -> unsafe
8. in conditional above -> unsafe
9. in conditional below -> unsafe

So the issue appears to happen during the line `if gm.fen != game.fen:`. 
To verify, lets put it in the compare fen funcion, and see if we get a partial block of invalid moves.
    - Looks like putting the log in between the definition and return (short function) does not stop the error part way through
What about putting it in the validate_legal_moves function before call to fen_compare?
    - This does stop the functionality part way
