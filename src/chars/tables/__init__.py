from __future__ import annotations

from typing import TYPE_CHECKING

from .unicode import NUM_CODEPOINTS, TABLE_CFGS, make_tables

if TYPE_CHECKING:
    from char import Char

    from .unicode import Table

ByteTables = list[list[str]]


def _tables_from_chars(chars: list[Char]):
    width_map = [1] * NUM_CODEPOINTS
    for c in chars:
        if c.width < 0:
            width_map[c.code] = 3
        else:
            width_map[c.code] = c.width

    tables = make_tables(TABLE_CFGS, enumerate(width_map))
    return _make_byte_tables(tables)


def _make_byte_tables(tables: list[Table]) -> ByteTables:
    byte_tables = []
    for (i, table) in enumerate(tables):
        if i == len(tables) - 1:
            table.indices_to_widths()
        byte_tables.append(list(map(lambda b: '0x{:02X}'.format(b), table.to_bytes())))
    return byte_tables


class Tables():

    @classmethod
    def from_chars(cls, chars: list[Char]) -> ByteTables:
        return _tables_from_chars(chars)
