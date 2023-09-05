#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Follow a SuperTicTacToe game “live” on your terminal."""
from dataclasses import dataclass
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from .sttt import Cell, Game, Matrix


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
class Winner:
    game: Game

    def __rich__(self, /) -> str:
        players = f"[red]{self.game.X.name}[/red] vs [blue]{self.game.O.name}[/blue]"
        match game.winner:
            case Cell._:
                info = "Game On!"
            case Cell.x:
                info = f"[red]{self.game.X.name} Wins![/red]"
            case Cell.o:
                info = f"[blue]{self.game.X.name} Wins![/blue]"
            case Cell.i:
                info = f"Draw!"
        return f"[bold]{players}\n{info}[/]"


@dataclass(slots=True)
class Board:
    matrix: Matrix[Matrix[Cell]]

    def __rich__(self, /) -> str:
        return (
            " ╻ ".join(["╷".join([" "*3]*3)]*3) + "\n" +  # first row
            ("\n" + "━╋━".join(["━".join(["━"*3]*3)]*3) + "\n").join([  # thick separator
                ("\n" + " ┃ ".join(["┼".join(["─"*3]*3)]*3) + "\n").join([  # thin separator
                    " ┃ ".join([
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
            + "\n" + " ╹ ".join(["╵".join([" "*3]*3)]*3)  # last row
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
    winner = Winner(game)
    layout = Layout()
    layout.split_column(
        Layout(Align.center(winner), name="top", size=2),
        Layout(Align.center(results), name="center", size=9),
        Layout(Align.center(board), name="bottom"),
    )
    with Live(layout):
        winner = game.play(sleep=.5)


if __name__ == "__main__":
    from .randobot import RandoBot
    game = Game(
        RandoBot(),
        RandoBot(),
    )
    live(game)
