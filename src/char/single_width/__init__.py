from __future__ import annotations

from typing import TYPE_CHECKING

from . import latin_letters_and_others

if TYPE_CHECKING:
    from char import Char


def is_include(char: Char) -> bool:
    return latin_letters_and_others.is_include(char)
