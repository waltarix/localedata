from char.emoji import _all, _code_ranges


def test__all():
    assert len(_all()) == 418


def test__code_ranges():
    assert _code_ranges().length == 61
