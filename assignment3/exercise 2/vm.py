import sys
from architecture import NUM_REG, OPS, OP_MASK, OP_SHIFT, RAM_LEN
import io

COLUMNS = 4
DIGITS = 8


# [init]
class VirtualMachine:
    def __init__(self):
        self.initialize([])
        self.prompt = ">>"

    def initialize(self, program):
        assert len(program) <= RAM_LEN, "Program too long"
        self.ram = [
            program[i] if (i < len(program)) else 0
            for i in range(RAM_LEN)
        ]
        self.ip = 0
        self.reg = [0] * NUM_REG
# [/init]

    # [fetch]
    def fetch(self):
        instruction = self.ram[self.ip]
        self.ip += 1
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return [op, arg0, arg1]
    # [/fetch]

    # [run]
    def run(self):
        running = True
        while running:
            op, arg0, arg1 = self.fetch()
            if op == OPS["hlt"]["code"]:
                running = False
            elif op == OPS["ldc"]["code"]:
                self.reg[arg0] = arg1
            elif op == OPS["ldr"]["code"]:
                self.reg[arg0] = self.ram[self.reg[arg1]]
            elif op == OPS["cpy"]["code"]:
                self.reg[arg0] = self.reg[arg1]
            # [skip]
            # [store]
            elif op == OPS["str"]["code"]:
                self.ram[self.reg[arg1]] = self.reg[arg0]
            # [/store]
            # [add]
            elif op == OPS["add"]["code"]:
                self.reg[arg0] += self.reg[arg1]
            # [/add]
            elif op == OPS["sub"]["code"]:
                self.reg[arg0] -= self.reg[arg1]
            # Task 3.1 start
            # [/inc]
            elif op == OPS["inc"]["code"]:
                self.reg[arg0] += 1
            # [/dec]
            elif op == OPS["dec"]["code"]:
                self.reg[arg0] -= 1
            # [/swp]
            elif op == OPS["swp"]["code"]:
                temp = self.reg[arg0]
                self.reg[arg0] = self.reg[arg1] 
                self.reg[arg1] = temp
            
                
            # Task 3.1 end
            # [beq]
            elif op == OPS["beq"]["code"]:
                if self.reg[arg0] == 0:
                    self.ip = arg1
            # [/beq]
            elif op == OPS["bne"]["code"]:
                if self.reg[arg0] != 0:
                    self.ip = arg1
            elif op == OPS["prr"]["code"]:
                print(self.prompt, self.reg[arg0])
            elif op == OPS["prm"]["code"]:
                print(self.prompt, self.ram[self.reg[arg0]])
            # [/skip]
            else:
                assert False, f"Unknown op {op:06x}"
    # [/run]

def main_for_tests(vm_instance, input_path, output_path):
    #using StringIO to capture output
    with io.StringIO() as buffer, open(input_path, "r") as reader:
        #redirect stdout to the buffer
        old_stdout = sys.stdout
        sys.stdout = buffer

        try:
            lines = [ln.strip() for ln in reader.readlines()]
            program = [int(ln, 16) for ln in lines if ln]
            vm_instance.initialize(program)
            vm_instance.run()

            #get the contents of the buffer (captured output)
            captured_output = buffer.getvalue()
        finally:
            #restorinf the original stdout
            sys.stdout = old_stdout

        # Return the captured output
        return captured_output
