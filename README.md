# lox_engine
Lox engine is a rudimentary chess engine and game platform where you can play against Lox, a basic chess engine, or against your friends in timed or untimed games.


## What is lox_engine?
Currently, lox_engine is a terminal based chess game that parses algebraic notation to make moves on the board. After each move, lox_engine will display the game board and the FEN string representing the game, so you can save or transport the game to another instance of lox_engine or any other chess platform.

### What are the limitations?
As of the current version, lox_engine lacks these key features that many a complete chess engine would have:
    
    - Detecting stalemate
    - Detecting checkmate
    - Exporting game to PGN
    - Graphic user interface for games
    - Ability to play against you

**That last point is key:** the whole idea of lox_engine is to play against you. It might never be a challenger to the likes of Stockfish or Leela Chess Zero, in fact it would probably get smoked, but I plan to write an engine that can play to at least a 2000 Elo level.

## Table of Contents:
 - [Installation](#installation)

 - [How to Use](#how-to-use)

 - [About](#about)


## Installation
Frankly, I don't know yet. I haven't built it yet.


## How to Use
To start lox_engine, navigate to its directory in your terminal. and run `uv run main.py` to start a new game.

> To start a game from a position with a FEN string, run: `uv run main.py "[FEN string]"`

![game start](imgs/game_startup.png)

## About

Made by Jeremy McKeegan
