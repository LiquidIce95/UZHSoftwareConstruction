
from typing import Any

class Fake:
    def __init__(self, func=None, default_return=None):
        self.func = func
        self.default_return = default_return
        self.calls = []
    
    def __call__(self, *args, **kwargs):
        self.calls.append([args,kwargs])
        if self.default_return is not None:
            return self.default_return
        if self.func is not None:
            return self.func(*args, **kwargs)


def fakeit(name, func=None, default_return=None):
    assert name in globals()
    fake = Fake(func,default_return)
    globals()[name] = fake
    return fake


def add(n1,n2):
    return n1 + n2

def test_add_real_function():
    assert add(2,3) == 5


def test_add_with_fake_return():
    fakeit("add",default_return=99)
    assert add(2,3) == 99


def test_fake_records_calls():
    fake = fakeit("add",default_return=99)
    assert add(2,3) == 99
    assert add(6,7) == 99
    assert fake.calls == [[(2, 3), {}], [(6, 7), {}]]

def mock_add(n1,n2):
    return 0

def test_add_with_fake_function():
    fakeit("add",func=mock_add)
    assert add(2,3) == 0

def test_add_with_fake_lambda_function():
    fakeit("add",func=lambda n1, n2: n1 * n2)
    assert add(2,3) == 6
