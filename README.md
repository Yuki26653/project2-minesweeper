## Minesweeper in Python

A simple console-based Minesweeper game written in Python.
This project focuses on implementing the core game logic and
handling cell expansion in a clean and understandable way.

### Features
- 9×9 grid with randomly placed mines
- Separate hidden board (ground truth) and visible board
- Open and flag commands via simple text input
- Console display of the game state

### What I focused on
- Separating game logic from the player’s view of the board
- Computing adjacent mine counts for each cell
- Implementing cell expansion when opening a zero-value cell

For the expansion logic, I used a queue-based approach to
gradually reveal connected empty cells, while keeping track
of visited positions to avoid repeated processing.

### How to play
- `o row col` : open a cell
- `f row col` : flag or unflag a cell
- `quit`      : exit the game

### Notes
- The game runs entirely in the console
- This project was mainly used to practice grid logic,
  boundary checks, and basic queue / stack-style thinking
