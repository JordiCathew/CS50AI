# Minesweeper

AI that plays Minesweeper.

## Background

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).

## Requirements
This projects requires the pygame Python package.
In order to install it we run:

```bash
$ pip install pygame 
```

or

```bash
$ py - m pip install pygame
```

in latest releases.

## Usage

```bash
$ py runner.py
```


