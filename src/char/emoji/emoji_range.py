from __future__ import annotations

from code_range import CodeRange
from code_ranges import CodeRange


class EmojiRange(CodeRange):

    def is_wide(self) -> bool:
        return self.min >= 0x1F000
