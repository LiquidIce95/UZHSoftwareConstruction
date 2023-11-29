import pytest
from assembler import Assembler, main_test

TEST_ROOT = "Test_Files/Assembly/"
A_ROOT = "Assembly_Files/"
def call_assembler_for_test_files(input, output):
    main_test(Assembler, input, output)

def assert_equalitity_of_files(file_a, file_b):
    with open(file_a, "r") as a:
        a = a.read()
        # split both into lines and remove empty string from list
        a = list(filter(lambda x: x != '', a.split("\n")))

    with open(file_b, "r") as b:
        b = b.read()
        # split both into lines and remove empty string from list
        b = list(filter(lambda x: x != '', b.split("\n")))

    if len(a) == len(b):
        # loop through the files and compare each line
        for i, line in enumerate(a):
            assert line == b[i]
    else:
        return Warning("Files do not have the same length!")

def run(case, input):
    call_assembler_for_test_files(f"{input}.as", f"{input}.mx")
    assert_equalitity_of_files(f"{input}.mx", f"{case}_man.mx")

def test_1(case=f"{TEST_ROOT}test1", input=f"{A_ROOT}test1"):
    run(case, input)

def test_2(case=f"{TEST_ROOT}test2", input=f"{A_ROOT}test2"):
    run(case, input)

def test_3(case=f"{TEST_ROOT}test3", input=f"{A_ROOT}test3"):
    run(case, input)

def test_4(case=f"{TEST_ROOT}test4", input=f"{A_ROOT}test4"):
    run(case, input)

# These cases should raise errors
def test_inf_error(case=f"{TEST_ROOT}test_inf_error", input=f"{A_ROOT}test_inf_error"):
    with pytest.raises(KeyError):
        run(case, input)
