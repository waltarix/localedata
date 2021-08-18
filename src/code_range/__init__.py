from __future__ import annotations

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

    def __eq__(self, other: CodeRange) -> bool:
        return self.min == other.min and self.max == other.max
