from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from code_range import RangeOfCode
from code_ranges import CodeRanges

if TYPE_CHECKING:
    from char import Char

RANGES: list[RangeOfCode] = [
    (0x0000, 0x001F),
    (0x007F, 0x009F),
    (0x00AD, 0x00AD),
    (0x070F, 0x070F),
    (0x180B, 0x180E),
    (0x200B, 0x200F),
    (0x2028, 0x202E),
    (0x206A, 0x206F),
    (0xD800, 0xDFFF),
    (0xFEFF, 0xFEFF),
    (0xFFF9, 0xFFFB),
    (0xFFFE, 0xFFFF),
]


def is_include(char: Char) -> bool:
    return _ranges().is_include(char.code)


@lru_cache
def _ranges():
    return CodeRanges.from_range_of_code(RANGES)
