import pytest
import os
import disassemble_v2
from contextlib import contextmanager
import vm
import re
import assembler



#Helper function that creates the testfiles
@contextmanager
def create_temp_input_file(content):
    filename = "temp_input.mx"
    try:
        with open(filename, 'w') as file:
            file.write(content)
        yield filename
    finally:
        os.remove(filename)

def opcodes_setup(input_file):
    disassemble_v2.main_for_tests([input_file, "temp.as"])
    results = extract_opcodes("temp.as")
    os.remove("temp.as")
    return results

def extract_opcodes(file_path):
    with open(file_path, 'r') as file:
        return [line.split()[0] for line in file if line.strip() and ':' not in line]

def labels_setup(input_file):
    disassemble_v2.main_for_tests([input_file, "temp.as"])
    results = extract_label_positions("temp.as")
    os.remove("temp.as")
    return results


def extract_label_positions(file_path):
    positions = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line.endswith(':'):
                # Store the line number where the label is defined
                positions.append((line_number, None))
            elif '@' in line:
                # Update the last entry with the line number where the label is referenced
                if positions and positions[-1][1] is None:
                    positions[-1] = (positions[-1][0], line_number)
    return positions

def extract_last_number(output):
    # Find all occurrences of '>> ' followed by one or more digits
    matches = re.findall(r'>> (\d+)', output)

    # Check if there are any matches
    if matches:
        # Return the last match as an integer
        return int(matches[-1])
    else:
        # Return None or raise an error if no match is found
        return None

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
    disassemble_v2.main_for_tests([input_file, "output_tester.as"])
    assembler.main_for_tests(assemb, input_path="output_tester.as", output_path="transformed.mx")
    os.remove("output_tester.as")
    result = run_vm("transformed.mx")
    os.remove("transformed.mx")
    return result

#################  Testing the file format handling  #################

def test_wrong_input_extension_correct_output_extension():
    test_args = ["input_file.txt", "output_file.as"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

def test_correct_input_extension_wrong_output_extension():
    test_args = ["input_file.mx", "output_file.txt"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

def test_wrong_input_output_extensions():
    test_args = ["input_file.txt", "output_file.txt"]
    with pytest.raises(AssertionError) as excinfo:
        disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "Input has to be a .mx file, Output has to be a .as file"

#################  Testing the handling of wrong formats  #################

def test_non_hexadecimal_content():
    with create_temp_input_file("GHI1KL\n12A456") as temp_file:
        test_args = [temp_file, "output_hex.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_improperly_formatted_line_length():
    with create_temp_input_file("12345\n1234567") as temp_file:
        test_args = [temp_file, "output_length.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_improperly_formatted_line_space():
    with create_temp_input_file("123 45\n1234567") as temp_file:
        test_args = [temp_file, "output_space.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "File contains elements that do not match the mx format"

def test_empty_file():
    with create_temp_input_file("") as temp_file:
        test_args = [temp_file, "output_empty.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
    assert str(excinfo.value) == "File is empty"

#################  Testing the operation codes  #################

def test_wrong_opcode_to_low():
    opcodes = "020002\n000103\n000202\n000300\n000204\n000305\n000001"
    with create_temp_input_file(opcodes) as temp_file:
        test_args = [temp_file, "output.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
        assert "Unknown operation used" in str(excinfo.value)   # Replace with your specific error message

def test_wrong_opcode_to_high():
    opcodes = "02000F\n000103\n000202\n000302\n000204\n000305\n000001"
    with create_temp_input_file(opcodes) as temp_file:
        test_args = [temp_file, "output.as"]
        with pytest.raises(AssertionError) as excinfo:
            disassemble_v2.main_for_tests(test_args)
        assert "Unknown operation used" in str(excinfo.value)   # Replace with your specific error message

#################  Testing the operation codes placement and order  #################
def test_opcodes_comparison_1():
    assert opcodes_setup("test_disassembler_1.mx") == extract_opcodes("test_disassembler_1.as")

def test_opcodes_comparison_2():
    assert opcodes_setup("test_disassembler_2.mx") == extract_opcodes("test_disassembler_2.as")

def test_opcodes_comparison_3():
    assert opcodes_setup("test_disassembler_3.mx") == extract_opcodes("test_disassembler_3.as")

def test_opcodes_comparison_4():
    assert opcodes_setup("test_disassembler_4.mx") == extract_opcodes("test_disassembler_4.as")

def test_opcodes_comparison_5():
    assert opcodes_setup("test_disassembler_5.mx") == extract_opcodes("test_disassembler_5.as")

#################  Testing the labels  #################

def test_label_comparison_4():
    assert labels_setup("test_disassembler_4.mx") == extract_label_positions("test_disassembler_4.as")

def test_label_comparison_5():
    assert labels_setup("test_disassembler_5.mx") == extract_label_positions("test_disassembler_5.as")

#################  Testing final outcome and the expected results are the same  #################
def test_finanl_outcome_1():
    assert run_vm("test_disassembler_1.mx") == final_outcome_set_up("test_disassembler_1.mx")
    
def test_finanl_outcome_2():
    assert run_vm("test_disassembler_2.mx") == final_outcome_set_up("test_disassembler_2.mx")

def test_finanl_outcome_3():
    assert run_vm("test_disassembler_3.mx") == final_outcome_set_up("test_disassembler_3.mx")

def test_finanl_outcome_4():
    assert run_vm("test_disassembler_4.mx") == final_outcome_set_up("test_disassembler_4.mx")

def test_finanl_outcome_5():
    assert run_vm("test_disassembler_5.mx") == final_outcome_set_up("test_disassembler_5.mx")

