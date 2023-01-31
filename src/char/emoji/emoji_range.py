from code_range import CodeRange


class EmojiRange(CodeRange):

    def is_wide(self) -> bool:
        return self.min >= 0x1F000
