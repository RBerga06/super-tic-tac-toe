#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RandoBots: players who play random moves."""
from dataclasses import dataclass, field
import random
from typing import ClassVar
from typing_extensions import override

from .sttt import Coord, Player


@dataclass
class RandoBot(Player):
    _counter: ClassVar[int] = 0
    name: str = field(init=False)

    def __post_init__(self, /) -> None:
        self.name = f"RandoBot {type(self)._counter}"
        type(self)._counter += 1

    @override
    def choose(self, options: set[tuple[Coord, Coord, Coord, Coord]]) -> tuple[Coord, Coord, Coord, Coord]:
        return random.choice([*options])


__all__ = ["RandoBot"]
