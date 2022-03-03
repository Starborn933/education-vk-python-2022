import pytest


def test_one():
    assert 1 == 2


class Test:
    def test_two(self):
        assert 1 != 2


def check_zero_division(a, b):
    assert a / b


def test_negative():
    with pytest.raises(ZeroDivisionError):
        check_zero_division(1, 1)
        pytest.fail(reason="No ZeroDivisionError occured")
