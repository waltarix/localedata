from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from char import Char


def is_include(char: Char) -> bool:
    return char.is_ambiguous() and char.code < 0x02B0
