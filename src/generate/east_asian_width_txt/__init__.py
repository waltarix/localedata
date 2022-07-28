from char import Char
from chars import CharRanges


def generate(eaw: CharRanges):
    for char_range in eaw.ranges:
        codes = map(_formatter, char_range.minmax(unique=True))
        print('{};F'.format('..'.join(codes)))


def _formatter(char: Char):
    return f'{char.code:04X}'
