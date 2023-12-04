import pytest
import os
import disassemble
from contextlib import contextmanager
import vm
import re
import assembler

#helper function that creates the testfiles
@contextmanager
def create_temp_input_file(content):
    try:
        with open("temp_input.mx", 'w') as file:
            file.write(content)
        yield "temp_input.mx"
    finally:
        os.remove("temp_input.mx")

#setupu function for the op_code tests
def opcodes_setup(input_file):
    disassemble.main_for_tests([input_file, "temp.as"])
    results = extract_opcodes("temp.as")
    os.remove("temp.as")
    return results

#function that creates alist with all op_codes used
def extract_opcodes(file_path):
    with open(file_path, 'r') as file:
        return [line.split()[0] for line in file if line.strip() and ':' not in line]

#setup funciton for the label tests
def labels_setup(input_file):
    disassemble.main_for_tests([input_file, "temp.as"])
    results = extract_label_positions("temp.as")
    os.remove("temp.as")
    return results

#extracts all the lable postiions in a as file
def extract_label_positions(file_path):
    positions = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line.endswith(':'):
                #store the line number where the label is defined
                positions.append((line_number, None))
            elif '@' in line:
                #update the last entry with the line number where the label is referenced
                if positions and positions[-1][1] is None:
                    positions[-1] = (positions[-1][0], line_number)
    return positions

#funciton that extracts the last number from the captured vm output
def extract_last_number(output):
    #finding all occurrences of '>> ' followed by one or more digits
    matches = re.findall(r'>> (\d+)', output)

    #check if there are any matches
    if matches:
        #return the last match as an integer
        return int(matches[-1])
    else:
        #return None, which will then rais an assertion error if one file outputs somethig and the other not.
        return None

#function that handles the vm calls.
def run_vm(input_file):
    virt = vm.VirtualMachine()
    x = vm.main_for_tests(virt, input_file, "out.out")
    last_number = extract_last_number(x)
    try:
        os.remove("out.out")
    except OSError as e:
        print(f"Error: out.out : {e.strerror}")
    
    return last_number


def final_outcome_set_up(input_file):
    assemb = assembler.Assembler
    disassemble.main_for_tests([input_file, "output_tester.as"])
    assembler.main_for_tests(assemb, input_path="output_tester.as", output_path="transformed.mx")
    os.remove("output_tester.as")
    result = run_vm("transformed.mx")
    os.remove("transformed.mx")
    return result

#################  Testing the file format handling  #################

def test_wrong_input_extension_correct_output_extension():
    test_args = ["input_file.txt", "output_file.as"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

def test_correct_input_extension_wrong_output_extension():
    test_args = ["input_file.mx", "output_file.txt"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

def test_wrong_input_output_extensions():
    test_args = ["input_file.txt", "output_file.txt"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

#################  Testing the handling of wrong formats  #################

def test_non_hexadecimal_content():
    with create_temp_input_file("GHI1KL\n12A456") as temp_file:
        test_args = [temp_file, "output_hex.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_improperly_formatted_line_length():
    with create_temp_input_file("12345\n1234567") as temp_file:
        test_args = [temp_file, "output_length.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_improperly_formatted_line_space():
    with create_temp_input_file("123 45\n1234567") as temp_file:
        test_args = [temp_file, "output_space.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_empty_file():
    with create_temp_input_file("") as temp_file:
        test_args = [temp_file, "output_empty.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
    assert str(excinfo.value) == "File is empty"

#################  Testing the operation codes  #################

def test_wrong_opcode_to_low():
    opcodes = "020002\n000103\n000202\n000300\n000204\n000305\n000001"
    with create_temp_input_file(opcodes) as temp_file:
        test_args = [temp_file, "output.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
        assert "Unknown operation used" in str(excinfo.value)

def test_wrong_opcode_to_high():
    opcodes = "02000F\n000103\n000202\n000302\n000204\n000305\n000001"
    with create_temp_input_file(opcodes) as temp_file:
        test_args = [temp_file, "output.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble.main_for_tests(test_args)
        assert "Unknown operation used" in str(excinfo.value) 

#################  Testing the operation codes placement and order  #################

def test_opcodes_comparisons():
    for i in range(1, 6):
        mx_file = f"test_disassembler_{i}.mx"
        as_file = f"test_disassembler_{i}.as"
        assert opcodes_setup(mx_file) == extract_opcodes(as_file)

#################  Testing the labels  #################

def test_label_comparisons():
    for i in range(1, 6):
        mx_file = f"test_disassembler_{i}.mx"
        as_file = f"test_disassembler_{i}.as"
        assert labels_setup(mx_file) == extract_label_positions(as_file)

#################  Testing final outcome and the expected results are the same  #################

def test_final_outcomes():
    for i in range(1, 6):
        mx_file = f"test_disassembler_{i}.mx"
        assert run_vm(mx_file) == final_outcome_set_up(mx_file)

