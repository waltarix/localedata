from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from code_range import RangeOfCode
from code_ranges import CodeRanges

from . import latin_letters_and_others

if TYPE_CHECKING:
    from char import Char

RANGES: list[RangeOfCode] = [
    (0x24EB, 0x24FF),
    (0x2500, 0x254B),
    (0x2550, 0x2573),
    (0x2580, 0x258F),
    (0x2592, 0x2595),
    (0x25A0, 0x25A1),
    (0x25A3, 0x25A9),
    (0xE0A0, 0xE0D7),
]


def is_include(char: Char) -> bool:
    return _ranges().is_include(char.code) or latin_letters_and_others.is_include(char)


@lru_cache
def _ranges():
    return CodeRanges.from_range_of_code(RANGES)
