from pathlib import Path

EmojiData = Path('unicode/emoji-data.txt')

_east_asian_width = Path('unicode/EastAsianWidth.txt')
_custom_widths = list(Path('unicode/custom_width').glob('*'))
Widths = [_east_asian_width, *_custom_widths]
