#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Super Tic Tac Toe."""
from enum import IntEnum
from dataclasses import dataclass
from typing import Annotated, Iterator, Literal, cast
from annotated_types import Len

# The board is a 3x3x3x3 4D matrix:
# [
#   [g00, g01, g02],
#   [g10, g11, g12],
#   [g10, g21, g22],
# ]
# where each g** represents a tic-tac-toe board:
# g00 = [
#   [s00, s01, s02],
#   [s10, s11, s12],
#   [s20, s21, s22],
# ]
# where each s** square can be filled with one of three numbers:
#  +1: 'x'
#   0: empty square
#  -1: 'o'

type list3[T] = Annotated[list[T], Len(3, 3)]
type tuple3[T] = tuple[T, T, T]
type Matrix[T] = list3[list3[T]]
type Coord = Literal[1, 2, 3]

class Cell(IntEnum):
    i = 0b00  # invalid
    _ = 0b01  # empty square
    o = 0b10  # player 'o'
    x = 0b11  # player 'x'


def getRaw[T](board: Matrix[T], x: Coord, /) -> tuple3[T]:
    return cast(tuple3[T], tuple(board[x]))

def getCol[T](board: Matrix[T], y: Coord, /) -> tuple3[T]:
    return cast(tuple3[T], tuple(board[x][y] for x in range(3)))

def getDiag1[T](board: Matrix[T], /) -> tuple3[T]:
    return cast(tuple3[T], tuple(board[x][x] for x in range(3)))

def getDiag2[T](board: Matrix[T], /) -> tuple3[T]:
    return cast(tuple3[T], tuple(board[x][2-x] for x in range(3)))

def contains(board: Matrix[Cell], c: Cell, /) -> bool:
    for row in board:
        if c in row:
            return True
    return False

def matches(board: Matrix[Cell], c: Cell, /) -> Iterator[tuple[Coord, Coord]]:
    for x in range(3):
        row = board[x]
        for y in range(3):
            if row[y] == c:
                yield cast(tuple[Coord, Coord], (x, y))

def move(board: Matrix[Cell], x: Coord, y: Coord, m: Cell, /) -> Cell:
    if board[x][y] != Cell._:
        raise ValueError("Moves can only be played in empty squares.")
    board[x][y] = m
    if getRaw(board, x) == (m, m, m):
        return m
    if getCol(board, x) == (m, m, m):
        return m
    if x == y and getDiag1(board) == (m, m, m):
        return m
    if x + y == 2 and getDiag2(board) == (m, m, m):
        return m
    if contains(board, Cell._):
        return Cell._  # game is still going
    return Cell.i      # game is finished


@dataclass(slots=True)
class Game:
    board: Matrix[Matrix[Cell]]
    results: Matrix[Cell]

    def __init__(self, /) -> None:
        self.board = [[[[Cell._ for _3 in range(3)] for _2 in range(3)] for _1 in range(3)] for _0 in range(3)]
        self.results = [[Cell._ for _1 in range(3)] for _0 in range(3)]

    def _choices(self, X: Coord, Y: Coord, /) -> Iterator[tuple[Coord, Coord, Coord, Coord]]:
        board = self.board[X][Y]
        for x in range(3):
            for y in range(3):
                if board[x][y] == Cell._:
                    yield X, Y, cast(Coord, x), cast(Coord, y)

    def choices(self, last: tuple[Coord, Coord] | None = None, /) -> Iterator[tuple[Coord, Coord, Coord, Coord]]:
        """List all possible moves after a move was played at `last` spot on a mini-board."""
        if last is not None:
            x, y = last
            if self.results[x][y] != Cell._:
                # game in that mini-board already ended
                yield from self.choices(None)
                return
            yield from self._choices(x, y)
        for x in range(3):
            for y in range(3):
                yield from self._choices(cast(Coord, x), cast(Coord, y))