# No pytest solution using recently learned stuff
import pytest

from assembler import *
import threading

# Test with decorators and TestFixture in pytest

# How do I call from assemler?
def call_assembler_for_test_files(input, output):
    main_test(Assembler, input, output)

def assert_equaltity_of_files(file_a, file_b):
    # loop through the files and compare each line
    with open(file_a, "r") as a:
        a = a.read()
        # split both into lines and remove empty string from list
        a = list(filter(lambda x: x != '', a.split("\n")))

    with open(file_b, "r") as b:
        b = b.read()
        # split both into lines and remove empty string from list
        b = list(filter(lambda x: x != '', b.split("\n")))

    if len(a) == len(b):
        for i, line in enumerate(a):
            assert line == b[i]
    else:
        return Warning("Files do not have the same length!")

def run(case, input):
    call_assembler_for_test_files(input, input)
    assert_equaltity_of_files(input, case)

# def all_tests(case):
#    call_assembler_for_test_files(f"{case}.as", f"{case}.mx")
#    assert_equaltity_of_files(f"{case}.mx", f"{case}_man.mx")
#    print(f"Test case: {case} ran successfully.")

# TEST_CASES = {
#    "test1": all_tests,
#    "test2": all_tests,
#    "test3": all_tests,
#    "test4": all_tests
# }

# for key, val in TEST_CASES.items():
#    threading.Thread(target=val(key), args=(1,))

@pytest.fixture
def test_1(a, b):
    run(open("Test_Files/Assembly/test1_man.mx", "r").readlines(), open("Assembly_Files/test1.as"))
