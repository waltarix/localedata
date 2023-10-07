from chars import eaw_ranges


def test_eaw_ranges():
    ranges = eaw_ranges()
    assert ranges.length == 249
