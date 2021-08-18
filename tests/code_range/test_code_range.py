from code_range import CodeRange


def test_overlapping_range():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(20, 30)
    assert cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(10, 30)


def test_continuous_range():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(21, 30)
    assert not cr1.is_overlap(cr2)
    assert cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(10, 30)


def test_non_continuous_range():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(22, 30)
    assert not cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert not cr1.is_mergeable(cr2)


def test_intersecting_range():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(19, 30)
    assert cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(10, 30)


def test_overlapping_range_in_reverse_order():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(0, 10)
    assert cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(0, 20)


def test_continuous_range_in_reverse_order():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(0, 9)
    assert not cr1.is_overlap(cr2)
    assert cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(0, 20)


def test_non_continuous_range_in_reverse_order():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(0, 8)
    assert not cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert not cr1.is_mergeable(cr2)


def test_intersecting_range_in_reverse_order():
    cr1 = CodeRange(10, 20)
    cr2 = CodeRange(0, 11)
    assert cr1.is_overlap(cr2)
    assert not cr1.is_continuous(cr2)
    assert cr1.is_mergeable(cr2)
    assert cr1.merge(cr2) == CodeRange(0, 20)
