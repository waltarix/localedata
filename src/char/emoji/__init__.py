from __future__ import annotations

from functools import lru_cache, reduce
from operator import methodcaller
from typing import TYPE_CHECKING, cast

from code_ranges import CodeRanges
from ucd import EmojiData

from .emoji_range import EmojiRange
from .match_group import MatchedGroup
from .pattern import PATTERN

if TYPE_CHECKING:
    from char import Char


def is_include(char: Char):
    return _code_ranges().is_include(char.code)


@lru_cache
def _code_ranges():
    wides = filter(methodcaller('is_wide'), _all())
    squeezed = reduce(_squeeze, wides, [])
    return CodeRanges(list(squeezed))


def _all():
    emoji_ranges: list[EmojiRange] = []
    with EmojiData.open(mode='r') as ED:
        for line in ED:
            m = PATTERN.match(line)
            if m is None:
                continue
            mg = cast(MatchedGroup, m.groupdict())
            min = int(mg['min'], 16)
            max = int(mg['max'], 16) if mg['max'] else min
            emoji_ranges.append(EmojiRange(min, max))
    return emoji_ranges


def _squeeze(memo: list[EmojiRange], range: EmojiRange):
    try:
        if memo[-1].is_mergeable(range):
            memo[-1].merge(range)
        else:
            memo.append(range)
    except IndexError:
        memo.append(range)
    return memo
