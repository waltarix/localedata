import re

PATTERN = re.compile(
    r'''
        ^
        (?P<min>[0-9A-F]{4,6})
        (?:
          \.\.
          (?P<max>[0-9A-F]{4,6})
        )?
        \s+;\s+Emoji\s+
        \#
    ''',
    flags=re.VERBOSE
)
