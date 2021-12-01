from __future__ import annotations

import operator
from typing import Callable

RangeOfCode = tuple[int, int]


class CodeRange():
    min: int
    max: int

    @classmethod
    def from_range_of_code(cls, range_of_code: RangeOfCode) -> CodeRange:
        return cls(*range_of_code)

    def __init__(self, min: int, max: int) -> None:
        if min < max:
            self.min = min
            self.max = max
        else:
            self.min = min
            self.max = max

    def is_include(self, code: int) -> bool:
        return self.min <= code and code <= self.max

    def merge(self, other: CodeRange) -> CodeRange:
        self.min = min(self.min, other.min)
        self.max = max(self.max, other.max)
        return self

    def is_mergeable(self, other: CodeRange) -> bool:
        if self.is_overlap(other):
            return True
        return self.is_continuous(other)

    def is_continuous(self, other: CodeRange) -> bool:
        return self.max + 1 == other.min or self.min - 1 == other.max

    def is_overlap(self, other: CodeRange) -> bool:
        return self.is_include(other.min) or self.is_include(other.max)

    def __str__(self) -> str:
        return '({}, {})'.format(self.min, self.max)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CodeRange):
            return False
        return self.min == other.min and self.max == other.max

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __lt__(self, other: object) -> bool:
        return self._compare(operator.lt, other, is_less=True)

    def __le__(self, other: object) -> bool:
        return self._compare(operator.le, other, is_less=True)

    def __gt__(self, other: object) -> bool:
        return self._compare(operator.gt, other, is_greater=True)

    def __ge__(self, other: object) -> bool:
        return self._compare(operator.ge, other, is_greater=True)

    def _compare(self, operator: Callable, other: object, is_less: bool = False, is_greater: bool = False) -> bool:
        if not isinstance(other, CodeRange):
            raise TypeError()

        if is_less:
            if self.min == other.min:
                return operator(self.max, other.max)
            return operator(self.min, other.min)
        if is_greater:
            if self.max == other.max:
                return operator(self.min, other.min)
            return operator(self.max, other.max)

        raise ValueError()

    def __hash__(self) -> int:
        return hash((self.min, self.max))
