import pytest
from vm import VirtualMachine, main_test

TEST_ROOT = "Test_Files/Vm/"
A_ROOT = "Assembly_Files/"
V_ROOT = "Vm_Files/"

def call_vm_for_test_files(input, output):
    main_test(VirtualMachine, input, output)

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

def run(case, input, output):
    call_vm_for_test_files(f"{input}.mx", f"{output}.txt")
    assert_equalitity_of_files(f"{output}.txt", f"{case}_man.txt")

def test_1(case=f"{TEST_ROOT}test1", input=f"{A_ROOT}test1", output=f"{V_ROOT}test1"):
    run(case, input, output)

def test_2(case=f"{TEST_ROOT}test2", input=f"{A_ROOT}test2", output=f"{V_ROOT}test2"):
    run(case, input, output)

def test_3(case=f"{TEST_ROOT}test3", input=f"{A_ROOT}test3", output=f"{V_ROOT}test3"):
    run(case, input, output)

def test_4(case=f"{TEST_ROOT}test4", input=f"{A_ROOT}test4", output=f"{V_ROOT}test4"):
    run(case, input, output)

# These cases should raise errors
def test_ram(case=f"{TEST_ROOT}test_ram", input=f"{A_ROOT}test_ram", output=f"{V_ROOT}test_ram"):
    with pytest.raises(IndexError):
        run(case, input, output)

def test_inf_error(case=f"{TEST_ROOT}test_inf_error", input=f"{A_ROOT}test_inf_error", output=f"{V_ROOT}test_inf_error"):
    with pytest.raises(AssertionError):
        run(case, input, output)

# What would the additional problem be if we don't know that the assembler is correct?
# We could switch to the manually calculated test files