import sys

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
    with open(input_file, 'r') as infile:
        for line in infile:
            instruction = int(line.strip(), 16)
            asm_line, op = disassemble_instruction(instruction)
            asm_lines.append((asm_line, op))

    insert_labels(asm_lines)

    with open(output_file, 'w') as outfile:
        for line, _ in asm_lines:
            outfile.write(line + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python disassemble.py input_file.mx output_file.as")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        disassemble_file(input_file, output_file)
