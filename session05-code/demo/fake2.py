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


class ContextFake(Fake):
    def __init__(self, name, func=None, default_return=None):
        super().__init__(func,default_return)
        self.name = name
        self.original = globals()[name]

    def __enter__(self):
        assert self.name in globals()
        self.original = globals()[self.name]
        globals()[self.name] = self
        return self

    def __exit__(self,exc_type,exc_value,exc_traceback):
        globals()[self.name] = self.original


def sub(n1,n2):
    return n1 - n2

def test_checks_no_lasting_effects():
    assert sub(2,1) == 1
    try:
        with ContextFake("sub",default_return=123) as fake:
            assert sub(2,1) == 123
            assert len(fake.calls) == 1
            raise ValueError
    except Exception:
        print("There was an error")

    assert sub(2,1) == 1