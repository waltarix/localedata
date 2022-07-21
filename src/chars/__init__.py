from __future__ import annotations

from functools import lru_cache
from typing import cast

from char import Char
from ucd import Widths

from .char_ranges import CharRanges
from .match_group import MatchedGroup
from .pattern import PATTERN
from .tables import Tables


def wcwidth9_tables():
    return Tables.from_chars(all())


def eaw_ranges():
    filtered = filter(_eaw_filter, all())
    return CharRanges.from_chars(list(filtered))


def _eaw_filter(char: Char):
    if char.is_reserved():
        return False
    return char.is_double_width()


@lru_cache
def all():
    chars: dict[int, Char] = {}
    for Width in Widths:
        with Width.open(mode='r') as WD:
            for line in WD:
                m = PATTERN.match(line)
                if m is None:
                    continue
                mg = cast(MatchedGroup, m.groupdict())
                min = int(mg['min'], 16)
                max = int(mg['max'], 16) if mg['max'] else min
                props = {'width_prop': mg['width_prop'], 'data_prop': mg['data_prop'], 'comment': mg['comment']}
                for code in range(min, max + 1):
                    chars[code] = Char(code, **props)
    return sorted(chars.values())
