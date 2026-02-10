# lox_engine
Lox engine is a rudimentary chess engine and game platform where you can play against Lox, a basic chess engine, or against your friends in timed or untimed games.

## Brainstorming:
- [ ] Write board representation
    - [X] Should just show the board in the terminal for now
    - [ ] Input chess notation to CLI to move pieces, no logic for now
- [ ] Write FEN or PGN parser
    - [X] board to FEN
    - [ ] FEN to board setup
    - [ ] export game as PGN
    - [ ] import PGN as game
- [ ] Build classes for pieces
    - [ ] Write movement per piece
    - [ ] Write special moves:
        - [ ] en-passent
        - [ ] castling
        - [ ] promotion
- [ ] Write game state reader:
    - [ ] Before move is committed:
        - [ ] Check if move is valid
            - [ ] Can this piece make this move?
            - [ ] Will this move result in putting self in check?
            - [ ] Are you trying to capture your own piece?
        - [ ] If not valid, revert
    - [ ] After move is committed:
        - [ ] Check for promotion
        - [ ] Check for check
        - [ ] Check for stalemate
        - [ ] Check for checkmate
- [ ] Lox:
    - [ ] Write board-to-evaluation reader
    - [ ] Write search algorithm:
        - [ ] Look at first 20 moves found:
            - [ ] Best 5 get recursively searched to depth of 5 layers
            - [ ] Build map of positions to navigate
        - [ ] Make what move has the best outcome at layer 5
        - [ ] After opponent moves, see if this is still within searched positions
            - [ ] If it is, do recursive search to build out possibility library
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
        - 



### Packages that could be useful:
- uv virtual machine: I've always been running a vm when building in python, so this seems natural
- pygame: good for running the visual side of the game

## Table of Contents:
 - [Installation](#installation)

 - [How to Use](#how-to-use)

 - [About](#about)


## Installation
Frankly, I don't know yet. I haven't built it yet.


## How to Use
There isn't anything to use yet.

## About

Made by Jeremy McKeegan
