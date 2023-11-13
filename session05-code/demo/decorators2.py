
def wrap(func):
    def _inner(*args):
        print("before call")
        func(*args)
        print("after call")
    return _inner

@wrap
def original(value,value2):
    print(f"original: {value,value2}")

original("example","another thing")

