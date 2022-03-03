import pytest


def test_negative():
    errors = []
    for i in range(10):
        try:
            assert i % 2 == 0
        except AssertionError:
            errors.append(f'{i} not even')
    assert not errors


@pytest.mark.parametrize('i', list(range(10)))
def test_even2(i):
    """
    :param i: range of integers
    Parametrized test which checks that number if even.
    """
    assert i % 2 == 0
