from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from char import Char

EMOJI_MODIFIERS = (0x1F3FB, 0x1F3FF)

ZERO_WIDTH_DATA_PROP = {'Me', 'Mn', 'Cf'}


def is_include(char: Char) -> bool:
    if char.data_prop in ZERO_WIDTH_DATA_PROP:
        return True
    return EMOJI_MODIFIERS[0] <= char.code and char.code <= EMOJI_MODIFIERS[1]
