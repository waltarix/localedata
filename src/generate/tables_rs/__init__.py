from jinja2 import Environment, FileSystemLoader

from char import Char
from chars import CharRanges

env = Environment(loader=FileSystemLoader('templates'))


def generate(wcwidth9: CharRanges):
    template = env.get_template('tables.j2')
    rows = []
    for char_range in wcwidth9.ranges:
        min, max = map(_formatter, char_range.minmax())
        width = str(char_range.width).rjust(2)
        rows.append(f'({min}, {max}, {width}, {width})')
    print(template.render(ranges=rows))


def _formatter(char: Char):
    return "'\\u{{{code:x}}}'".format(code=char.code).rjust(12)
