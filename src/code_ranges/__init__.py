from __future__ import annotations

from bisect import bisect_left

from code_range import CodeRange, RangeOfCode


class CodeRanges():
    ranges: list[CodeRange]
    length: int
    maxes: list[int]

    @classmethod
    def from_range_of_code(cls, ranges_of_code: list[RangeOfCode]) -> CodeRanges:
        code_ranges = map(lambda roc: CodeRange.from_range_of_code(roc), sorted(ranges_of_code))
        return cls(list(code_ranges))

    def __init__(self, code_ranges: list[CodeRange]) -> None:
        self.ranges = code_ranges
        self.length = len(code_ranges)
        self.maxes = list(map(lambda r: r.max, self.ranges))

    def is_include(self, code) -> bool:
        index = bisect_left(self.maxes, code)
        if index == self.length:
            return False
        r = self.ranges[index]
        return r.is_include(code)
