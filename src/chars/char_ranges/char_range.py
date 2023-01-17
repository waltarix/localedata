from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from char import Char


class CharRange():
    min: Char
    max: Char
    width: int

    def __init__(self, char: Char) -> None:
        self.min = char
        self.max = char
        self.width = char.width

    def minmax(self, unique=False):
        if unique and self.min == self.max:
            return [self.min]
        return [self.min, self.max]

    def merge(self, other: Char):
        self.max = other

    def is_mergeable(self, other: Char):
        return self.max.is_mergeable(other)

    def is_range(self):
        return self.min != self.max
