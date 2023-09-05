#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Follow a SuperTicTacToe game “live” on your terminal."""
from dataclasses import dataclass
from rich import print
from rich.padding import Padding
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Group
from rich.columns import Columns
from rich.live import Live
from .sttt import Cell, Game, Matrix, Player


# -- Results -
#     ╷   ╷
#   X │ O │ #
#  ───┼───┼───
#   O │   │ X
#  ───┼───┼───
#   X │ O │ #
#     ╵   ╵
#
# --------------- Board ---------------
#     ╷   ╷   ╻   ╷   ╷   ╻   ╷   ╷
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   O │   │ X ┃ O │   │ X ┃ O │   │ X
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#  ━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   O │   │ X ┃ O │   │ X ┃ O │   │ X
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#  ━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   O │   │ X ┃ O │   │ X ┃ O │   │ X
#  ───┼───┼───╂───┼───┼───╂───┼───┼───
#   X │ O │ # ┃ X │ O │ # ┃ X │ O │ #
#     ╵   ╵   ╹   ╵   ╵   ╹   ╵   ╵
#



rich_cell = {
    Cell._: " ",
    Cell.i: "[bold]#[/]",
    Cell.x: "[bold red]X[/]",
    Cell.o: "[bold blue]O[/]",
}


@dataclass(slots=True)
class Board:
    matrix: Matrix[Matrix[Cell]]

    def __rich__(self, /) -> str:
        return (
            "╻".join(["╷".join([" "*3]*3)]*3) + "\n" +  # first row
            ("\n" + "╋".join(["┿".join(["━"*3]*3)]*3) + "\n").join([  # thick separator
                ("\n" + "╂".join(["┼".join(["─"*3]*3)]*3) + "\n").join([  # thin separator
                    "┃".join([
                        "│".join([
                            f" {rich_cell[self.matrix[X][Y][x][y]]} "
                            for y in range(3)
                        ])
                        for Y in range(3)
                    ])
                    for x in range(3)
                ])
                for X in range(3)
            ])
            + "\n" + "╹".join(["╵".join([" "*3]*3)]*3)  # last row
        )


@dataclass(slots=True)
class Results:
    matrix: Matrix[Cell]

    def __rich__(self, /) -> str:
        return "\n".join([
            "╷".join([" "*3]*3),  # first row
            "│".join([f" {rich_cell[self.matrix[0][y]]} " for y in range(3)]),
            "┼".join(["─"*3]*3),  # separator
            "│".join([f" {rich_cell[self.matrix[1][y]]} " for y in range(3)]),
            "┼".join(["─"*3]*3),  # separator
            "│".join([f" {rich_cell[self.matrix[2][y]]} " for y in range(3)]),
            "╵".join([" "*3]*3),  # last row
        ])


def live(game: Game, /) -> None:
    """Follow the given `game` live."""
    board = Board(game.board)
    results = Results(game.results)
    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(Align.center(board), name="bottom")
    )
    layout["top"].split_row(
        Layout("Info", name="left"),
        Layout(results, name="right"),
    )
    with Live(layout):
        winner = game.play(sleep=1)


if __name__ == "__main__":
    _b = Board([[[
            [Cell.x, Cell.o, Cell.i],
            [Cell.i, Cell._, Cell.x],
            [Cell.o, Cell.i, Cell._],
        ]*3]*3]*3
    )
    _r = Results([
        [Cell.x, Cell.o, Cell.i],
        [Cell.i, Cell._, Cell.x],
        [Cell.o, Cell.i, Cell._],
    ])
    layout = Layout()
    layout.split_column(
        Layout(name="top"),
        Layout(Align.center(_b), name="bottom")
    )
    layout["top"].split_row(
        Layout("Info", name="left"),
        Layout(_r, name="right"),
    )
    # print(repr(_b.__rich__()))
    # print(Panel.fit(Group(_b, _r), title="X (99999) vs O (0)"))
    print(layout)
