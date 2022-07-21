from __future__ import annotations

import operator
from functools import lru_cache
from typing import Callable, Optional

from . import emoji, non_printable, single_width, zero_width

WIDTH_MAP = {
    'N': 1,
    'Na': 1,
    'H': 1,
    'A': 2,
    'W': 2,
    'F': 2,
}


class Char():
    code: int
    width_prop: str
    data_prop: str
    comment: str
    _width: Optional[int] = None

    def __init__(
        self,
        code: int,
        width_prop: Optional[str] = None,
        data_prop: Optional[str] = None,
        comment: Optional[str] = None
    ) -> None:
        self.code = code
        self.width_prop = width_prop or ''
        self.data_prop = data_prop or ''
        self.comment = comment or ''

    def is_well_known(self) -> bool:
        return self.code < 0x00A0

    def is_ambiguous(self) -> bool:
        return self.width_prop == 'A'

    @property
    @lru_cache
    def width(self) -> int:
        if self.is_soft_hyphen():
            return 1
        elif self.is_non_printable():
            return -1
        elif self.is_zero_width():
            return 0
        elif self.is_single_width():
            return 1
        elif self.is_emoji():
            return 2
        return WIDTH_MAP[self.width_prop]

    def is_soft_hyphen(self) -> bool:
        return self.code == 0x00AD

    def is_reserved(self) -> bool:
        return self.comment.startswith('<reserved-')

    def is_double_width(self) -> bool:
        return self.width == 2

    def is_non_printable(self) -> bool:
        return non_printable.is_include(self)

    def is_zero_width(self) -> bool:
        return zero_width.is_include(self)

    def is_single_width(self) -> bool:
        return single_width.is_include(self)

    def is_emoji(self) -> bool:
        return emoji.is_include(self)

    def is_mergeable(self, other: Char) -> bool:
        return (self.code + 1 == other.code) and self.width == other.width

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Char):
            return False
        return self.code == other.code

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __lt__(self, other: object) -> bool:
        return self._compare(operator.lt, other)

    def __le__(self, other: object) -> bool:
        return self._compare(operator.le, other)

    def __gt__(self, other: object) -> bool:
        return self._compare(operator.gt, other)

    def __ge__(self, other: object) -> bool:
        return self._compare(operator.ge, other)

    def _compare(self, operator: Callable, other: object) -> bool:
        if not isinstance(other, Char):
            raise TypeError()
        return operator(self.code, other.code)

    def __hash__(self) -> int:
        return hash(self.code)
