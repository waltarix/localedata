from chars import eaw_ranges, wcwidth9_ranges


def test_eaw_ranges():
    ranges = eaw_ranges()
    assert ranges.length == 244


def test_wcwidth9_ranges():
    ranges = wcwidth9_ranges()
    assert ranges.length == 1545
