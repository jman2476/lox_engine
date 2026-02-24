# Lox Engine ToDo list:
This is a list of all things that need to be implemented, and those that have been successfully implemented

### Packages that could be useful:
- uv virtual machine: I've always been running a vm when building in python, so this seems natural
- colorama
- pygame: good for running the visual side of the game

## Brainstorming:
- [ ] Write board representation
    - [X] Should just show the board in the terminal for now
    - [X] Input chess notation to CLI to move pieces, no logic for now
- [ ] Write FEN or PGN parser
    - [X] board to FEN
    - [X] FEN to board setup
    - [ ] export game as PGN
    - [ ] import PGN as game
- [X] Build classes for pieces
    - [X] Write movement per piece
    - [X] Write special moves:
        - [X] en-passent
        - [X] castling
        - [X] promotion
- [ ] Write game state reader:
    - [X] Before move is committed:
        - [X] Check if move is valid
            - [X] Can this piece make this move?
            - [X] Will this move result in putting self in check?
            - [X] Are you trying to capture your own piece?
        - [X] If not valid, revert
    - [ ] After move is committed:
        - [X] Check for promotion
        - [X] Check for check
        - [ ] Check for stalemate
        - [ ] Check for checkmate
- [ ] Refactor all parsing functions to efficiently use regex

- [ ] Testing:
    - [ ] Finish writing tests for all move parsing functions
        - [ ] Parse pawn move
        - [ ] Parse pawn capture
        - [ ] Parse en passent
        - [ ] Parse pawn promotion
        - [ ] Parse castling
        - [ ] Parse piece move
            - [ ] Standard move
            - [ ] Standard capture
            - [ ] Disambiguated moves
        - [ ] Piece lookback
    - [ ] Write tests for stalemate
    - [ ] Write tests for checkmate
    - [ ] Write tests for finding all possible moves in a position

- [ ] GUI:
    - [ ] Make gui in PyGame
    - [ ] Include panel for error messages
    - [ ]

- [ ] Lox:
    - [ ] Write move finder
    - [ ] Write board-to-evaluation reader
    - [ ] Write search algorithm:
        - [ ] Look at first 20 moves found:
            - [ ] Best 5 get recursively searched to depth of 5 layers
            - [ ] Build map of positions to navigate
        - [ ] Make what move has the best outcome at layer 5
        - [ ] After opponent moves, see if this is still within searched positions
            - [ ] If it is, do revcursive search to build out possibility library
            - [ ] If it isn't, delete incompatible positions, and do recursive search

## Parsing Move notation:
- Types of move notation:
    - e5 -> simple pawn move
    - exf5 -> pawn cature
    - Bg8 -> minor/major standard move
    - Bxe3 -> minor/major capture
    - 0-0 || O-O || o-o -> king-side castle
    - 0-0-0 || O-O-O || o-o-o -> queen-side castle
    - e1=Q -> pawn promotion
    - Rae7 -> file disambiguation
    - R1e7 -> rank disambiguation
    - Re2e7 -> full disambiguation
- First char is 0, o, O:
    - castling, check castling possibility
    - look if king is in check
    - look if king would move through check
    - if fine, do move
- if 2 chars: pawn move
    - look for pawn 1 or 2 ranks before
- if 3 chars: minor/major piece move
    - read type of piece
    - look back from square for relavent piece
        - look in each direction
- if 4 chars: 
    - if contains 'x': Capture
    - Otherwise, disampbiguation or promotion
    - Promotion indicated by '='

- Better idea:
    - check for castling first
    - look at last two characters, they will be the target square
        - if there is '+' or '#', skip
        - if there is a 'Q', 'N', 'R', or 'B', parse for pawn promotion
    - from there, read backward toward first character
        - LMAO, fuck that -> Just use a regex, budd