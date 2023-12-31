import sys
import re

OPS = {
    0x1: "hlt --",
    0x2: "ldc rv",
    0x3: "ldr rr",
    0x4: "cpy rr",
    0x5: "str rr",
    0x6: "add rr",
    0x7: "sub rr",
    0x8: "beq rv",
    0x9: "bne rv",
    0xA: "prr r-",
    0xB: "prm r-",
    0xC: "inc r-",
    0xD: "dec r-",
    0xE: "swp rr"
}

OP_MASK = 0xFF
OP_SHIFT = 8
BRANCH_OPS = {0x8, 0x9}  # opcodes for beq and bne

def disassemble_instruction(instruction):
    op = instruction & OP_MASK
    instruction >>= OP_SHIFT
    arg0 = instruction & OP_MASK
    instruction >>= OP_SHIFT
    arg1 = instruction & OP_MASK

    assert op in OPS, f"Unknown operation used {op}"

    asm_op, fmt = OPS[op].split()

    args = []
    if 'r' in fmt:
        args.append(f"R{arg0}")
    if 'r' in fmt[1:]:
        args.append(f"R{arg1}")
    elif 'v' in fmt:
        args.append(str(arg1))

    return f"{asm_op} {' '.join(args)}", op


def insert_labels(asm_lines):
    label_count = 1
    label_map = {}
    for i, (line, op) in enumerate(asm_lines):
        if op in BRANCH_OPS:
            target_line = int(line.split()[-1])
            # Adjust for zero-based indexing
            label = label_map.setdefault(target_line, f"L{label_count:03d}")
            if label == f"L{label_count:03d}":
                label_count += 1
            # Replace only the last part of the line with the label
            line_parts = line.split()
            line_parts[-1] = f"@{label}"
            line = ' '.join(line_parts)
        asm_lines[i] = (line, op)

    # Adjust label insertion point
    for target_line, label in label_map.items():
        asm_lines[target_line] = (f"{label}:\n{asm_lines[target_line][0]}", None)

def disassemble_file(input_file, output_file):
    asm_lines = []

    #iterating over all the lines in the .mx file
    with open(input_file, 'r') as in_file:

        #testing if the file passed to the disassembler is emtpy
        assert len(in_file.read()) != 0, "File is empty"

        #resetting the reader, so that non-empty files get executed corretly
        in_file.seek(0)
        for line in in_file:
            #checking if the lines are in hexadecimal
            assert re.match(r'^[0-9A-Fa-f]{6}$', line.strip()), "File contains elements that do not match the mx format"
            #adding the lines with a changed format to the list from which the .as file will be constructed
            asm_lines.append(disassemble_instruction(int(line.strip(), 16)))

    #adding the labels to the assembly code
    insert_labels(asm_lines)

    #writing the ouput file
    with open(output_file, 'w') as out_file:
        out_file.write("".join(line + "\n" for line, _ in asm_lines))

def main_for_tests(files):
    assert files[0].endswith(".mx") and files[1].endswith(".as"), "Input has to be a .mx file, Output has to be a .as file"
    disassemble_file(files[0], files[1])

def main():
    assert len(sys.argv) == 3, "Usage: python disassemble.py input_file.mx output_file.as"
    assert sys.argv[1][-3:] == ".mx" and sys.argv[2][-3:] == ".as", "Input has to be a .mx file, Output has to be a .as file"
    disassemble_file(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
