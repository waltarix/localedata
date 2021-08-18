from __future__ import annotations

from functools import lru_cache, reduce
from typing import TYPE_CHECKING

from .char_range import CharRange

if TYPE_CHECKING:
    from char import Char


class CharRanges():
    ranges: list[CharRange]

    @classmethod
    def from_chars(cls, chars: list[Char]) -> CharRanges:
        char_ranges = reduce(_squeeze, chars, [])
        return cls(char_ranges)

    def __init__(self, char_ranges: list[CharRange]) -> None:
        self.ranges = char_ranges

    @property
    @lru_cache
    def length(self) -> int:
        return len(self.ranges)


def _squeeze(memo: list[CharRange], char: Char):
    try:
        if memo[-1].is_mergeable(char):
            memo[-1].merge(char)
        else:
            memo.append(CharRange(char))
    except IndexError:
        memo.append(CharRange(char))
    return memo
