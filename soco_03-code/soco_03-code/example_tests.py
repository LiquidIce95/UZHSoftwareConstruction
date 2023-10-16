def square(n):
    r = n * n
    return r


def division(a,b):
    assert b != 0
    r = a / b
    return r


real_output = square(2)
expected_output = 4
assert real_output == expected_output


real_output = division(4,2)
expected_output = 2
assert real_output == expected_output

