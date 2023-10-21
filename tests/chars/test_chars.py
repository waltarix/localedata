from chars import all as all_chars, eaw_ranges


def test_eaw_ranges():
    ranges = eaw_ranges()
    assert ranges.length == 246


def has_custom_width(min: int, max: int):
    chars = filter(lambda char: min <= char.code <= max, all_chars())
    return all(char.custom_width for char in chars)


def test_regional_indicators():
    assert has_custom_width(0x1F1E6, 0x1F1FF)


def test_private_use_area():
    assert has_custom_width(0x100000, 0x10FFFD)
