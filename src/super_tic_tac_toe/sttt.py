#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: reportConstantRedefinition=false
"""Super Tic Tac Toe."""
from enum import IntEnum
from dataclasses import dataclass, field
from itertools import permutations
import time
from typing import Annotated, Iterator, Literal, Protocol, cast
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
    i = 0b00  # invalid/draw
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
    if getCol(board, y) == (m, m, m):
        return m
    if x == y and getDiag1(board) == (m, m, m):
        return m
    if x + y == 2 and getDiag2(board) == (m, m, m):
        return m
    if contains(board, Cell._):
        return Cell._  # game is still going
    return Cell.i      # game is finished


class Player(Protocol):
    name: str
    rating: float

    def choose(self, options: set[tuple[Coord, Coord, Coord, Coord]], /) -> tuple[Coord, Coord, Coord, Coord]:
        ...


ELO_0 = 800.00  # inital rating
ELO_K = 40

def deltaElo(X: float, O: float, result: Literal[Cell.x, Cell.i, Cell.o], /) -> tuple[float, float]:
    EX = 1 / (1 + 10 ** ((O - X)/400))  # expected score X
    EO = 1 - EX                         # expected score O
    match result:
        case Cell.x:  # x wins
            SX, SO = 1, 0
        case Cell.i:  # draw
            SX, SO = .5, .5
        case Cell.o:  # o wins
            SX, SO = 0, 1
    return ELO_K * (SX - EX), ELO_K * (SO - EO)


@dataclass(slots=True)
class Game:
    X: Player
    O: Player
    rated:   bool = True
    players: dict[Literal[Cell.x, Cell.o], Player] = field(init=False)
    last_p:  Literal[Cell.x, Cell.o] = Cell.x  # 'x' starts first
    last_m:  tuple[Coord, Coord, Coord, Coord] | None = None
    board:   Matrix[Matrix[Cell]] = field(init=False)
    results: Matrix[Cell]         = field(init=False)
    winner:  Cell                 = Cell._  # game on

    def __post_init__(self, /) -> None:
        self.board = [[[[Cell._ for _3 in range(3)] for _2 in range(3)] for _1 in range(3)] for _0 in range(3)]
        self.results = [[Cell._ for _1 in range(3)] for _0 in range(3)]
        self.players = {Cell.x: self.X, Cell.o: self.O}

    def next_p(self, /) -> Literal[Cell.o, Cell.x]:
        match self.last_p:
            case Cell.o:
                return Cell.x
            case Cell.x:
                return Cell.o

    def _choices(self, X: Coord, Y: Coord, /) -> Iterator[tuple[Coord, Coord, Coord, Coord]]:
        board = self.board[X][Y]
        for x in range(3):
            for y in range(3):
                if board[x][y] == Cell._:
                    yield X, Y, cast(Coord, x), cast(Coord, y)

    def choices(self, /) -> Iterator[tuple[Coord, Coord, Coord, Coord]]:
        """List all possible moves for the next player."""
        last_move = self.last_m
        if last_move is not None:
            _X, _Y, x, y = last_move
            if self.results[x][y] == Cell._:
                # game there has not ended yet
                yield from self._choices(x, y)
                return
        for X in range(3):
            for Y in range(3):
                if self.results[X][Y] == Cell._:
                    yield from self._choices(cast(Coord, X), cast(Coord, Y))

    def play1turn(self, /) -> None:
        if self.winner != Cell._:
            raise ValueError("Game ended!")
        p = self.last_p = self.next_p()
        X, Y, x, y = choice = self.players[p].choose({*self.choices()})
        self.winner = move(self.results, X, Y, move(self.board[X][Y], x, y, p))
        self.last_m = choice

    def play(self, /, *, sleep: float = 0) -> Literal[Cell.x, Cell.o, Cell.i]:
        while self.winner == Cell._:
            self.play1turn()
            if sleep:
                time.sleep(sleep)
        dX, dO = deltaElo(self.X.rating, self.O.rating, self.winner)
        self.X.rating += dX
        self.O.rating += dO
        return self.winner


@dataclass
class Tournament:
    players: list[Player]

    def games(self, /) -> Iterator[Game]:
        for X, O in permutations(self.players, 2):
            yield Game(X, O)

    def play(self, /) -> None:
        for game in self.games():
            game.play()
