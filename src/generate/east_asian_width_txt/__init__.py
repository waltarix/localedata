from linecache import getline

from char import Char
from chars import CharRanges
from chars.char_ranges.char_range import CharRange
from ucd import EastAsianWidth

from ..util.jinja2 import get_template


def generate(eaw: CharRanges):
    eaw_filepath = str(EastAsianWidth)
    template = get_template('EastAsianWidth.txt.j2')
    print(
        template.render(
            line1=getline(eaw_filepath, 1).strip(),
            line2=getline(eaw_filepath, 2).strip(),
            values=map(_to_values, eaw.ranges),
        )
    )


def _to_hex(char: Char):
    return f'{char.code:04X}'


def _to_values(char_range: CharRange):
    if char_range.is_range():
        number_of_itmes = '[{}]'.format(char_range.max.code - char_range.min.code + 1)
        comment = 'DUMMY..DUMMY'
    else:
        number_of_itmes = ''
        comment = 'DUMMY'

    return (
        '{};F'.format('..'.join(map(_to_hex, char_range.minmax(unique=True)))).ljust(16),
        number_of_itmes.rjust(7),
        comment,
    )
