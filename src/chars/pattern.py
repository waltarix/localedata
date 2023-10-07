import re

PATTERN = re.compile(
    r'''
        ^
        (?P<min>[0-9A-F]{4,6})
        (?:
          \.\.
          (?P<max>[0-9A-F]{4,6})
        )?
        \s+
        ;
        \s+
        (?P<width_prop>[^ ]+)
        \s+
        \#
        (?:
          \ (?P<data_prop>[^ ]+)
          \ (?:\s*\[\d+\])?
        )?
        \s+
        (?P<comment>.+)
    ''',
    flags=re.VERBOSE
)
