import pytest

from char import Char


def char(value: int) -> Char:
    return Char(value)


def test_eq():
    assert char(1) == char(1)
    assert not char(1) != char(1)


def test_ne():
    assert char(1) != char(2)
    assert not char(1) == char(2)


def test_lt():
    assert not char(1) < char(0)
    assert not char(1) < char(1)
    assert char(1) < char(2)

    with pytest.raises(TypeError):
        char(1) < 2
    with pytest.raises(TypeError):
        1 < char(2)


def test_le():
    assert not char(1) <= char(0)
    assert char(1) <= char(1)
    assert char(1) <= char(2)

    with pytest.raises(TypeError):
        char(1) <= 2
    with pytest.raises(TypeError):
        1 <= char(2)


def test_gt():
    assert char(1) > char(0)
    assert not char(1) > char(1)
    assert not char(1) > char(2)

    with pytest.raises(TypeError):
        char(1) > 2
    with pytest.raises(TypeError):
        1 > char(2)


def test_ge():
    assert char(1) >= char(0)
    assert char(1) >= char(1)
    assert not char(1) >= char(2)

    with pytest.raises(TypeError):
        char(1) >= 2
    with pytest.raises(TypeError):
        1 >= char(2)
