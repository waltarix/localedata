import os
import pathlib
from functools import lru_cache
from pathlib import Path
from typing import Self


class UCDPath(Path):
    # cf. https://github.com/python/cpython/pull/31691
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour  # type: ignore

    def __new__(cls: type[Self], *args) -> Self:
        self = super().__new__(cls, *args)
        return self

    @lru_cache
    def is_custom_width(self) -> bool:
        return self.match('unicode/custom_width/*')


EmojiData = UCDPath('unicode/emoji-data.txt')

EastAsianWidth = UCDPath('unicode/EastAsianWidth.txt')
_custom_widths = list(UCDPath('unicode/custom_width').glob('*'))
Widths = [EastAsianWidth, *_custom_widths]
