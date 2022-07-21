import pytest

from code_range import CodeRange


def code_range(min: int, max: int) -> CodeRange:
    return CodeRange(min, max)


def test_eq():
    assert code_range(1, 5) == code_range(1, 5)
    assert not code_range(1, 5) != code_range(1, 5)


def test_ne():
    assert code_range(1, 5) != code_range(1, 6)
    assert not code_range(1, 5) == code_range(1, 6)


def test_lt():
    assert not code_range(1, 1) < code_range(0, 0)
    assert not code_range(1, 1) < code_range(0, 1)
    assert not code_range(1, 1) < code_range(0, 2)
    assert not code_range(1, 1) < code_range(1, 1)
    assert code_range(1, 1) < code_range(1, 2)
    assert code_range(1, 1) < code_range(2, 2)
    assert code_range(1, 1) < code_range(2, 3)

    assert not code_range(1, 3) < code_range(0, 0)
    assert not code_range(1, 3) < code_range(0, 1)
    assert not code_range(1, 3) < code_range(0, 2)
    assert not code_range(1, 3) < code_range(0, 3)
    assert not code_range(1, 3) < code_range(0, 4)
    assert not code_range(1, 3) < code_range(1, 1)
    assert not code_range(1, 3) < code_range(1, 2)
    assert not code_range(1, 3) < code_range(1, 3)
    assert code_range(1, 3) < code_range(1, 4)
    assert code_range(1, 3) < code_range(2, 2)

    with pytest.raises(TypeError):
        assert code_range(0, 1) < 1
    with pytest.raises(TypeError):
        assert 1 < code_range(0, 1)


def test_le():
    assert not code_range(1, 1) <= code_range(0, 0)
    assert not code_range(1, 1) <= code_range(0, 1)
    assert not code_range(1, 1) <= code_range(0, 2)
    assert code_range(1, 1) <= code_range(1, 1)
    assert code_range(1, 1) <= code_range(1, 2)
    assert code_range(1, 1) <= code_range(2, 2)
    assert code_range(1, 1) <= code_range(2, 3)

    assert not code_range(1, 3) <= code_range(0, 0)
    assert not code_range(1, 3) <= code_range(0, 1)
    assert not code_range(1, 3) <= code_range(0, 2)
    assert not code_range(1, 3) <= code_range(0, 3)
    assert not code_range(1, 3) <= code_range(0, 4)
    assert not code_range(1, 3) <= code_range(1, 1)
    assert not code_range(1, 3) <= code_range(1, 2)
    assert code_range(1, 3) <= code_range(1, 3)
    assert code_range(1, 3) <= code_range(1, 4)
    assert code_range(1, 3) <= code_range(2, 2)

    with pytest.raises(TypeError):
        assert code_range(0, 1) <= 1
    with pytest.raises(TypeError):
        assert 1 <= code_range(0, 1)


def test_gt():
    assert code_range(1, 1) > code_range(0, 0)
    assert code_range(1, 1) > code_range(0, 1)
    assert not code_range(1, 1) > code_range(0, 2)
    assert not code_range(1, 1) > code_range(1, 1)
    assert not code_range(1, 1) > code_range(1, 2)
    assert not code_range(1, 1) > code_range(2, 2)
    assert not code_range(1, 1) > code_range(2, 3)

    assert code_range(1, 3) > code_range(0, 0)
    assert code_range(1, 3) > code_range(0, 1)
    assert code_range(1, 3) > code_range(0, 2)
    assert code_range(1, 3) > code_range(0, 3)
    assert not code_range(1, 3) > code_range(0, 4)
    assert code_range(1, 3) > code_range(1, 1)
    assert code_range(1, 3) > code_range(1, 2)
    assert not code_range(1, 3) > code_range(1, 3)
    assert not code_range(1, 3) > code_range(1, 4)
    assert code_range(1, 3) > code_range(2, 2)
    assert not code_range(1, 3) > code_range(2, 3)

    with pytest.raises(TypeError):
        assert code_range(0, 1) > 1
    with pytest.raises(TypeError):
        assert 1 > code_range(0, 1)


def test_ge():
    assert code_range(1, 1) >= code_range(0, 0)
    assert code_range(1, 1) >= code_range(0, 1)
    assert not code_range(1, 1) >= code_range(0, 2)
    assert code_range(1, 1) >= code_range(1, 1)
    assert not code_range(1, 1) >= code_range(1, 2)
    assert not code_range(1, 1) >= code_range(2, 2)
    assert not code_range(1, 1) >= code_range(2, 3)

    assert code_range(1, 3) >= code_range(0, 0)
    assert code_range(1, 3) >= code_range(0, 1)
    assert code_range(1, 3) >= code_range(0, 2)
    assert code_range(1, 3) >= code_range(0, 3)
    assert not code_range(1, 3) >= code_range(0, 4)
    assert code_range(1, 3) >= code_range(1, 1)
    assert code_range(1, 3) >= code_range(1, 2)
    assert code_range(1, 3) >= code_range(1, 3)
    assert not code_range(1, 3) >= code_range(1, 4)
    assert code_range(1, 3) >= code_range(2, 2)
    assert not code_range(1, 3) >= code_range(2, 3)

    with pytest.raises(TypeError):
        assert code_range(0, 1) >= 1
    with pytest.raises(TypeError):
        assert 1 >= code_range(0, 1)
