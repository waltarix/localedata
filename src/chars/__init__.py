from __future__ import annotations

from functools import lru_cache
from typing import cast

from char import Char
from ucd import EastAsianWidth

from .char_ranges import CharRanges
from .match_group import MatchedGroup
from .pattern import PATTERN


def wcwidth9_ranges():
    filtered = filter(_wcwidth9_filter, all())
    return CharRanges.from_chars(list(filtered))


def eaw_ranges():
    filtered = filter(_eaw_filter, all())
    return CharRanges.from_chars(list(filtered))


def _wcwidth9_filter(char: Char):
    return not char.is_well_known()


def _eaw_filter(char: Char):
    if char.is_reserved():
        return False
    return char.is_double_width()


@lru_cache
def all():
    chars: list[Char] = []
    with EastAsianWidth.open(mode='r') as EAW:
        for line in EAW:
            m = PATTERN.match(line)
            if m is None:
                continue
            mg = cast(MatchedGroup, m.groupdict())
            min = int(mg['min'], 16)
            max = int(mg['max'], 16) if mg['max'] else min
            props = {'width_prop': mg['width_prop'], 'data_prop': mg['data_prop'], 'comment': mg['comment']}
            chars.extend(Char(code, **props) for code in range(min, max + 1))
    return chars