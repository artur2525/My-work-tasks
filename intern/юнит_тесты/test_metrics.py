import metrics


def test_profit() -> None:
    '''test profit'''
    assert metrics.profit([1, 2, 3], [1, 1, 1]) == 3

def test_margin() -> None:
    '''test margin'''
    assert metrics.margin([1, 2, 3], [1, 1, 1]) == 3/6

def test_markup() -> None:
    '''test markup'''
    assert metrics.markup([1, 2, 3], [1, 1, 1]) == 1
