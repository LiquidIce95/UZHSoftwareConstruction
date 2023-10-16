import pprint

def sign(value):
    if value < 0:
        return "-"
    else:
        return "+"


def test_sign_negative():
    value = -3
    expected_value = "-"
    actual_value = sign(value)
    assert actual_value == expected_value

def test_sign_positive():
    assert sign(1) == "+"

def test_sign_problem():
    assert sign(2) == "-"

def test_sign_error():
    assert sgn(2) == "-"


def run_tests():
    results = {"pass":0,"fail":0,"error":0}
    all_tests = find_tests("test_")
    for test in all_tests:
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] = results["fail"] + 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")


def find_tests(prefix):
    tests = []
    for (name, func) in globals().items():
        if name.startswith(prefix):
            tests.append(func)
    return tests

run_tests()