## Exercise 1

### The tester for the assembler

**comparing files**

If the assembler.py file runs correctly it will save its output into a predefined 
".mx" file. Because I calculated the ".mx" files manually for each assembler file
I need a function that compares the code in both files. In my case that is the 
``assert_equality_of_files(file_a, file_b)`` function. It creates a list for each 
line in a file. But we have to be careful to ignore empty lines of code. For that
I used a lambda function.

```python 
a = list(filter(lambda x: x != '', a.split("\n")))
```

next up we make sure that both lists have the same length. If they do we iterate 
through each line comparing the two strings having the same list index.

**running the assembler from the testfile**

next up we need a function that calls the main function of the assembler. For 
that I had to write a new main function in the ```assembly.py``` file, because 
the standard function listens to a call from the CLI. I made a slight modification. 

```python 
def main_test(assember_cls, file_input, file_output):
    reader = open(file_input, "r")
    writer = open(file_output, "w")
    lines = reader.readlines()
    assembler = assember_cls()
    program = assembler.assemble(lines)
    for instruction in program:
        print(instruction, file=writer)
```

The test function takes the assembly file and the desired output file as arguments. 
We call it from the ```call_assembler_for_test_files(input, output)``` in the 
``assembly_test.py`` file.

We are almost through the code. For aesthetic reasons I created the ```run(case, input)```
function that calls ``assert_equalitity_of_files`` and ``call_assembler_for_test_files``

**Automatic testing**

I wrote a total of 6 assembly files. It is not nice to write all 6 (basically) same 
functions after another and takes too much time. No programmer likes to repeat 
code. That is the reason why I made use of pytest parameterization with the decorator 

```python
@pytest.mark.parametrize(parameters, [list of arguments])
```

next up I only had to write one more test that expects an error.

**Files for the assembler**

The assembly input files are located in the Assembly_Files folder together with 
the output files of the assembler. My manually calculated files are located in the 
Test_Files/Assembly folder. 

### The tester for the vm

The ```vm_test.py``` is analogical to the architecture of the ``assembler_test.py`` file. 
For that reason I will skip the explaination of the ```call_vm_for_test_files```, 
``call_vm_for_test_files`` and the ``run`` function. The same goes for the 
parameterization decorator. Only difference is that the vm tester takes 
three inputs. Further we have three additional tests one for ram space, one for an undefined 
operation and one for an incorrect hexadecimal value.

**Assumptions**

The tests assume the assembler is correct. If the assembler were faulty we could 
use the manually calculated "_man" files instead.

**Files for the vm**

Input files are located in the Assembly_Files directory manually calculated files in the 
Test_Files/Vm directory. Output files will be saved to the Vm_Files Folder.

### The assembly test files (/Assembly_Files)

**Test1 to Test4**

Those are the assembly codes I wrote to test the 11 basic operations.

**test_key_error**

Makes use of an undefined operation "pow".

**test_ram**

Allocates an illegal amount of ram for an array.

### The vm test files (also in /Assembly_Files)

**test1 to test4**

Those are the hexcodes to test the 11 basic operations.

**test_assert_error**

Uses a hexcode for an undefined operation

**test_false_hex**

Uses a value that is not a valid hexstring

**test_ram**

Uses an invalid amount of ram

### Test coverage

For the test coverage I used the pytest configuration. I have defined 
that in the ``.pytest.ini`` file.

```
[pytest]
python_files =
    *_test.py
addopts = --cov assembler --cov vm
```

When running the ```pytest``` command in the CLI pytest automatically looks 
for any file ending with ```_test.py```. For the coverage it uses the flag 
```--cov Module_Name```. For some reason it is not possible to append two 
files with the coverage flag. That is why I had to call the flag twice. now, When running the 
command ```pytest``` in the CLI, pytest actually runs:

```pytest --cov assembler --cov vm```

**Coverage percentage**

When running the coverage test it does not run to a 100%. A large part of this is due to the 
``main(*_cls)`` function. I do not have a test that runs the vm or assembler from the CLI. 
That means the only thing that could go wrong in my test is if the ```sys.argv``` library fails 
or the code crashes from the commandline.

## Task 2

### Disassembler
#### The disassemble_file function:
The global variables in the disassemle.py file are:
```python
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
BRANCH_OPS = {0x8, 0x9}
```

OPS is of course a dictionary that maps the hexadecimal code to the, in the lecture assigned, operaitons and their argument format. OP_MASK is later used to assing the bits to their funcitonality, as well as OP_SHIFT and BRANCH_OPS are finaly used to input the labels.

As required the disassembler works by using the following command:
```
python disassemble.py input_file.mx output_file.as
```

But we have added two different main functions so that the code can not only be called from the command line, a funcitonality added by the main funciton using the sys module to enable command line support, but also from another programm, in our case the test_disassemble.py file. This funcitonality is handled by the main_for_tests function. 

Both functions first check if the diassembler is given the correect input. Meaning if the disassemble.py file received an input in the mx format and an output file in the as format.

In case of the main():
```python
    assert len(sys.argv) == 3, "Usage: python disassemble.py input_file.mx output_file.as"
    assert sys.argv[1][-3:] == ".mx" and sys.argv[2][-3:] == ".as", "Input has to be a .mx file, Output has to be a .as file"
```

And in the main_for_tests():
```python
    assert len(files) == 2, "Usage: ['input_file.mx', output_file.as]"
    assert files[0].endswith(".mx") and files[1].endswith(".as"), "Input has to be a .mx file, Output has to be a .as file"
```

After this they both call the disassemble_file function which takes the input and output file as input. This function starts by reading the given mx file and then tests if the provided file is empty. If it is the funciton throws an AssertionError telling its user "File is empty". 
We decided to do this, because there is no reason to disassemble a empty file, given the output would of course be also empty, but more important we thought that an empty output file could lead to the user, if he did by mistake input an empty file, to look for bugs or mistakes in other parts of their code, which would be another one of those debugging sessions that could have been prevented if the simnple mistake was found. By simply thorwing an error when using it like this we prevent this scenario. 

When having passed this test, we have to reset the reader to the first line, which we do by using the seek() function:
```python
    in_file.seek(0)
```

Then, while iterating over the lines of the inpput file, we test if the lines fit the expected format, meaning six characters in hexadecimal. We use the match() function, from the regular expression module after having striped the line with line.strip() function. We do not remove any whitespace between the characters given that this would be a wrong format any way.
```python
    re.match(r"^[0-9A-Fa-f]{6}$", line.strip())
```

The regular expression pattern we are matching the lines against, allows them to pass if they contain 6 characters, which can be a number from 0 to 9 or a letter, either in upper or lower case from A-F, the hexadecimal format. 

Then we append the result of the call to the disassemble_instruction function to, a at the beginning initiated, list:
```python
    as_lines.append(disassemble_instruction(int(line.strip(), 16)))
```

When all lines have been processed, the pass them on to the insert_labels function which adds labels to the assembly code and then att the end we iterate over all the lines and write them into the ouput file:
```python
    with open(output_file, 'w') as out_file:
        out_file.write("".join(line + "\n" for line, _ in as_lines))
```

We simply concatinate the line of assembly code with an "\n" and then the ouput file is done. 

#### The disassemble_instruction function:
The disassembly of the instructions starts with the same bit-wise operation so assign the correct parameters to their corresponding labels, as seen in the vm.py file.
```python
    op = instruction & OP_MASK
    instruction >>= OP_SHIFT
    arg0 = instruction & OP_MASK
    instruction >>= OP_SHIFT
    arg1 = instruction & OP_MASK
```

After this the function checks if the operation which the user wants to perform is a recognised one, by checking if the hex code is in the OPS dictionary. If not, the funciton throws an AssertionError and informs the user about the error made. 

If the above test is passed, the funciton gets the operation code and its argument structure from the OPS dictionary and splits them up accordingly. After this a list is initialized that will hold the arguments of the mx code which are at the end used to construct the assembly code.

In section after the list is initialized we determin what registers or values the mx code contained and append the arguments list with the string version of them:
```python 
    if 'r' in fmt:
        args.append(f"R{arg0}")
    if 'r' in fmt[1:]:
        args.append(f"R{arg1}")
    elif 'v' in fmt:
        args.append(str(arg1))
```

At the end the funciton formats the operation code and its arguemnts returns them with the hex_code of the operaiton, which will be needed in the labeling process. 
```python
    return f"{as_op} {' '.join(args)}", op
```

#### The inster_label function:
The insert_label function takes a list as input and modifies it in-place. We decided to do this given the clear link between the disassemble_file function and the inster_label function and to keep the code simple and cleaner, wothout the need to have multiple copies of the same object. In a larger more complex system, for example if the disassmbler would be part of a bigger construct, we might no have decided to do so depending of course on the context. 

After initializing a counter, which is later used to add numbers to the labels, and a dictionary keeps track of which labels are used with which target line, the function iterates over the list containing the assembly code lines and the hexadecimal code.

If the hexadecimal code is mapped to a branching operation, the funciton will add a label to the assembly code.
```pyhton
    for i, (line, op) in enumerate(as_lines):
        if op in BRANCH_OPS:
```

First the the targeted line is extracted and then mapped to a default lable, if there does not already exist, which is then stored in the label_map dictionary. If the label was new the labal count is incremented by one.
```pyhton
    target_line = int(line.split()[-1])
    label = label_map.setdefault(target_line, f"L{label_count:03d}")
    if label == f"L{label_count:03d}":
        label_count += 1
```

Then the target line number, where the branch points to, in the assembly code is replaced with the @L00X label and then the line is updated in the in list with the assembly code lines.
```pyhton
    line_parts = line.split()
    line_parts[-1] = f"@{label}"
    line = ' '.join(line_parts)
```

At the end the function all the lines are iterated over again to add the L00X: labels, which are placed where the target lines pointed to.
```python
 for target_line, label in label_map.items():
    as_lines[target_line] = (f"{label}:\n{as_lines[target_line][0]}", None)
```

This very simple approach creates a lable, when ever there is a branching opeartion in the mx code. This is the only way we see this work, given the .mx file does not contain any context about where to put labels and where not. This is the same reason we did not add support for arrays, given that it would have created an @array label with every ldc operation in the resulting assembly code. 

We tought about other methods, such as creating a dictionary where the user could add values that would indicate known arrays, or a label that indicated a data structure but this would defeat the simplcity of the disassembler. Another method we thought of was to keep track of the number of times a particular memory address was referenced, and then add labels based on a certain threshold. But this would only be a heuristic approach and would most likely not lead to a satisfactory result. Thus we decided against the adding of support for arrays.

### Example input_file.mx
The example input_file.mx contains the code that describes a programm, that first assigns R0 to 0, then R1 to 22 and R3 to 2. Then it creates a loop and increases R0 until it strores the number 22. Then it adds 22 to 22 resulting in 44 being stored in R0, and later 2 is subtracted from 44 resulting in the final output of 42, the answer to the ultimate question of fife, the universe, and everything. 

If the file is disassembled, the result shows that the disassembler create a lables L001, and thus a loop, at the position required.

### Pytest file
To maximise the testing possibilities we modified the assembler.py file as well as the vm.py file. The changed them in a way that allows us to call them in the test_disassemble.py file. We added a main_for_tests funciton to both of them. 

We added the io module to the vm.py file to us to capture the output of the virtual machine, without chaning any of the logic, to ensure that the ouputs are still correct and based on the logic created before. The main_for_test function in the vm.py file does creates an in-memory StringIO buffer and redirects the standard output to it,which allows the function to collect all output generated during the virtual machine's execution. The function opens the specified input file containing the program code, which is then processed and executed by the virtual machine. After running the program, the function retrieves the output from the StringIO buffer and restores the standard output to its original state. This captured output is then returned. 
```python
    with io.StringIO() as buffer, open(input_path, "r") as reader:
        old_stdout = sys.stdout
        sys.stdout = buffer

        try:
            lines = [ln.strip() for ln in reader.readlines()]

            ...

            captured_output = buffer.getvalue()
        finally:
            sys.stdout = old_stdout

        return captured_output
```

In the assembler.py file the main_for_tests functiono takes assembler_cls, input_path, and output_path as parameters. This allows the function to be more flexible and to be called with different inputs and outputs which is needed in the pytest file. 

The test_dis_assemble.py file uses the modules import pytest os, which is used to setup files for tests and later teardown the test-setup, for example here:
```python
    def opcodes_setup(input_file):
        disassemble.main_for_tests([input_file, "temp.as"])
        results = extract_opcodes("temp.as")
        os.remove("temp.as")
        return results
```

from contextlib it uses contextmanager, which is used for setup and teardown as well as can be seen here:
```python
    @contextmanager
    def create_temp_input_file(content):
```

and finaly the test file uses python regular expression to, re, to modify the output captured by the StringIO buffer to allow us to compare the ouput of the vm:
```python
    matches = re.findall(r'>> (\d+)', output)
```

In addition it of cours imports the vm, the disassember as well as the assembler. 

#### Helper functions:
##### The create_temp_input_file function:
This function is a context manager for creating and using a temporary file with specified content. It creates a file, allows the calling code to use it within a with block, and ensures the file is deleted afterwards for cleanup.

##### The opcodes_setup function:
This function disassembles an input file, extracts opcodes from the resulting assembly code, deletes the temporary file, and returns the opcodes. As the names says it is used as a setup function for all the test, that test the correctness of the opcodes.

##### The extract_opcodes function:
This function reads a file and returns a list of the first word (opcode) from each line that is not a label definition.

##### The labels_setup function:
This function disassembles an input file, extracts label positions from the resulting assembly, deletes the temporary file, and returns the label positions. It is used as a setup fuction for all test trying to assess the correcntes of the labels and their positioningss.

##### The extract_label_positions function:
This function reads an assembly file and returns a list of line numbers where labels are defined and referenced.

##### The extract_last_number function:
This function parses a string, in this context, the ouput of the vm, to find and return the last number following the pattern '>> ', or None if no match is found.

##### The run_vm function:
This function runs the virtual machine on an input file, extracts the last number from its output, deletes the output file, and handles any file deletion errors.

##### The final_outcome_set_up:
his function assembles, disassembles, and then reassembles an input file, runs a virtual machine on the final output, deletes all intermediate files, and returns the last number from the VM's output. This function is used to assess if the output of the vm, of a file, that has gone through the disassembler is the same as before it was disassemnled.

#### The tests:
##### test_wrong_input_extension_correct_output_extension: 
This tests that the disassembler raises an AssertionError when provided with an input file having the wrong extension (.txt) but the correct output file extension (.as).

##### test_correct_input_extension_wrong_output_extension: 
Here we check if an AssertionError is raised when the input file has the correct extension (.mx) but the output file has the wrong extension (.txt).

##### test_wrong_input_output_extensions: 
This Verifies that an AssertionError is raised when both input and output files have incorrect extensions, which is tested using .txt endings.

##### test_non_hexadecimal_content: 
In this Test we look for an AssertionError when the disassembler processes a file containing non-hexadecimal content, indicating a format mismatch.

##### test_improperly_formatted_line_length: 
This checks for an AssertionError when the input file contains lines of incorrect length, a format issue.

##### test_improperly_formatted_line_space: 
We test for an AssertionError when the input file contains improperly spaced content, again a format error.

##### test_empty_file: 
This test verifies that an AssertionError is raised when the input file is empty.

##### test_wrong_opcode_to_low: 
This checks if an AssertionError is raised for opcodes that are not supported by the disassmbler.

##### test_wrong_opcode_to_high: 
This test tests for an AssertionError when encountering opcodes that are not supported

##### test_opcodes_comparisons: 
Here we compare opcodes extracted from multiple .mx files with those from corresponding .as files to ensure they match. We have a control .as file which at the end is compared to the ouput .as file resulting from using the disassembler on a .mx file.

##### test_label_comparisons: 
This compares label positions extracted from multiple .mx files with those from corresponding .as files for consistency. The .as file is again the control and the .mx file is processed by the disassembler.

##### test_final_outcomes: 
This test checks if the final outcomes from running a virtual machine on multiple .mx files match the expected results set up by a specific setup function. The .mx is first run directly by the vm, to create a control values. The helper funciton then uses the disassmbler on the .mx file, then the assembler and then runs it thourgh the vm. 

The tests can be started with the terminal command pytest when executing it from the exercise 2 subfolder. 


## Task 3

As always we tried to respect the design choices in the architecture.

### increment and decrement

```
inc R0
dec R0
```

implemented in the same section as the other operations in vm.py


```python
            elif op == OPS["inc"]["code"]:
                self.reg[arg0] += 1
            # [/dec]
            elif op == OPS["dec"]["code"]:
                self.reg[arg0] -= 1

```


### swap values 

swaps two the values of two registers without affencting the values of other registers

```
swp R2 R1


```

implemented in the same section as the other operations in vm.py

```python
            elif op == OPS["swp"]["code"]:
                temp = self.reg[arg0]
                self.reg[arg0] = self.reg[arg1] 
                self.reg[arg1] = temp

```

pretty self explanatory


### Reverse array in place

to prove the correctness of the algorithm we refer to the comments of the algorithm in example_3_3.as file, this is the file where its implemented.

Invariants:

R0 and R1 store the address of the first element and the last element of the subarray which is not reversed yet.

this holds for the first iteration until comment 4. between 4 and 5 the values are swapped and the addresses of R0 and R1 unchanged. at 5 the left pointer (refernce to R0) is incremented, since R0 has been storing the address to the first element it now has the address to the second element. between 6 and 7 the difference of the addresses are computed. we jump to :end only if they equal. if this is true for the first iteration then we are finished. if not the right pointer ( reference to R1) is decremented so it stores now the address to the second last element.


hence we proved the invariant for the first iteration. Now lets assume for some iteration k the invariant is true. we repeat the arguments from the previous paragraph and conclude by induction that it indeed is an invariant.

hence at 4 we are always swapping the first and last elements of the not reversed subarray. if the difference is more or equal to 1, we first increment R0 so the difference can then be only 0 so we skip to :end and the algorithm terminates. this also proves the correctness since only the necessary pairs are swapped.


for testing only modify two things:

in the .data section the array size, per default it is 30

and at comment 

```# modify array_length here, at least 1*********************```

at the `ldc R1 17` instruction set the array length (actual size used in algorithm), note that the algorithm assumes length to be at least 1 since for 0 the array is empty and there are no elements to reverse.

## Task 4

Since Greg admitted in the lecture that his architecture makes no sense and was designed that way only for educational purposes, we decided to design only one debugger class **VirtaulMachineBase** in which all functionality is in. Furthermore we made sure to keep all functions small in size and never more than 3 nested (3 identation levels deep) although there are few excpetions. We also kept the handlers dictionaray and strucutre with the "_do_" functions.

to use the debugger run `python vm_debugger.py watch.mx` where watch.mx is the compiled assembly programm.

One Major change apart from moving everything into one file is the interact function:

```python
def interact(self, addr):
        """
        copied from vm_entend.py
        """
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                command = self.read(f"{addr:06x} [{prompt}]> ")
                """
                    now we split possible args from command
                """

                comm_args = command.split(" ")

                """now we set the command variable to the command"""
                command = comm_args[0]
                """default value for args"""
                args = comm_args[1:]

                """checking if command is sound"""
                if not command:
                    continue
                
                elif command not in self.handlers:
                    """use search algorithm for user commannd task 4.3"""
                    command = self.searchComm(command)

                    if command == False:
                        continue

                """if there were args we must check if command supports them """
                fun = self.handlers[command]
                fun_arg_count = 0

                if(len(args)>0):
                    fun_arg_count = fun.__code__.co_argcount


                if args != [] and fun_arg_count <3:
                    """if command does not support augemnts"""
                    self.write(f"command does not support arguments") 
                    continue
                
                elif args != [] and fun_arg_count == 3:
                    interacting = fun(self.ip,args)

                else:
                    """execute this if its a command without args"""
                    interacting = fun(self.ip)
            except EOFError:
                self.state = VMState.FINISHED
                interacting = False

```

we first seperate the arugments from the command, check if its a valid command and then check if the command even supports arguments.

with these changes, any operation that wants now to support arguments just has to add a default argument like here:

```python
    def _do_add_breakpoint(self, addr, arg):

    #just add args=[]
    def _do_add_breakpoint(self, addr, args=[]):

```

and we also search with the search algorithm if a command is not in the dictionary handlers.

and the second major change:

```python
def run(self):
        """
        copied from vm_break.py
        """
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)

            """check if any value has changed in the watch"""
            """we make copy to avoid change in list error since self.watchs can be changed in loop"""
            to_wacht = [addr for addr in self.watchs]
            for addr in to_wacht:
                if type(addr) is int and self.watchs[addr] != self.ram[addr]:
                    self.write(f"watch triggered at {addr}")
                    self.show()
                    self.watchs[addr] = self.ram[addr]
                    self.interact(self.ip)
                    self.ip += 1
                    self.execute(op, arg0, arg1)
                    continue
                elif type(addr) is str and self.watchs[addr] != self.reg[int(addr[1:])]:
                    self.write(f"watch triggered at R{int(addr[1:])}")
                    self.show()
                    self.watchs[addr] = self.reg[int(addr[1:])]
                    self.interact(self.ip)
                    self.ip += 1
                    self.execute(op, arg0, arg1)
                    continue


            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                op, arg0, arg1 = self.decode(original)
                self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)

            else:
                if self.state == VMState.STEPPING:
                    self.interact(self.ip)
                self.ip += 1
                self.execute(op, arg0, arg1)
```

here we first check if an address is being watched. We first tried to implement the watch just like breaks but that made it impossible to check if the value has changed (since the value at that address is a watch and not the original value anymore). Its for sure not the most efficient solution. But considering time constraints of development, decreasing development time seemed to be more important.




### Show Memory Range

The basic functionality of the `memory` command printed the entire memory. Since this appears useful we decided to keep this functionality.

So writing 

```
000000 [bcdimqrsw]> memory
```

results in 

```
IP      = 000000
R000000 = 000000
R000001 = 000000
R000002 = 000000
R000003 = 000000
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000000

 breaks 

 watchs 
```

As you might notice we also added a breaks and watchs section, which prints all memory addresses which are being watched or are occupied by an break operation.

We cover those later.

By specifying one address, the content of that address gets printed

```
000000 [bcdimqrsw]> memory 3
  00000a
```

And prints the memory range if two addresses are specified


```
000000 [bcdimqrsw]> memory 3 9
  00000a  030005  010202  020006  010204  000207  030209
```

to achieve this we use the following helper function

```python
def showBetweenMemo(self,args):
        """
            helper function for task 4.1
            @args : list of one ore two memory addresses
        """

        assert(0<len(args),"no memory address")
        assert(len(args)<=2,"too many addresses")

        """print memory between two addresses"""
        base = int(args[0])

        if(len(args)==2):
            top = int(args[1])
        else:
            top = base
        
        output = ""

        self.assert_is_address(top)
        self.assert_is_address(base)

        while base <= top:
            output += f"  {self.ram[base]:06x}"
            base += 1

        self.write(output)
```

which is called from `_do_show`

`

### Breakpoint Addresses

And so with the previous preparation allowing the `break` and `clear` commands to use specific addresses is very simpel.

```python
def _do_add_breakpoint(self, addr, args=[]):
        """
            @addr : current address the debugger is at
            @args : optional, some address to set the debugger at
            @returns : True if a berakpoint has been set
                        None if there already was a breakpoint
                        False if memory address was out of bounds
        """
        """copied from vm_break.py"""

        if(len(args)==1):
            args[0] = int(args[0])

            addr = args[0]

            self.assert_is_address(addr)

            

        if self.ram[addr] == OPS["brk"]["code"]:
                return
        self.breaks[addr] = self.ram[addr]
        self.ram[addr] = OPS["brk"]["code"]
        return True


def _do_clear_breakpoint(self, addr, args=[]):
        """
            @addr : current address the debugger is at
            @args : optional, some address to set the debugger at
            @returns : True if a berakpoint has been cleared
                        None if there was no breakpoint
                        False if memory address was out of bounds
        """

        if len(args)==1:
            args[0] = int(args[0])

            addr = args[0]

            self.assert_is_address(addr)

        if self.ram[addr] != OPS["brk"]["code"]:
                return
        self.ram[addr] = self.breaks[addr]
        del self.breaks[addr]
        return True
```

simply calling `break 3` or `clear 3` sets and clears a breakpoint at address 3

### Command Completion

The command completion is called automatically each time the user does not use a prefixed command and can be called manually from the user for two use cases , first for listing all commands and second for searching if a input results in a correct command.


`se` and `search` are reserved and call `_do_search_command` which calls self.searchComm(args)

```python
def searchComm(self,command=[]):
        """
            solves task 4.3
            search algorithm wich searches for command of user

            @command : the user input which we use to search for the command
            @returns : the found command or false if nothing
                        has been found
        """
        """if user calls search without specified command list all commands"""
        if(command == []):
            self.write(" list of all commands ")

            for command in self.handlers:
                self.write(f"{command}")
                "return empty matches"
            
            return False

        """if user calls directly search the command will come as a list"""
        if(isinstance(command,list)):
            command = command[0]

        assert(command is str,"command is not a string")

        """now lets search for what the user could possibly mean"""
        self.write(f"is searching command {command}")
        commands = [keys for keys in self.handlers]

        commands.sort()
        
        matches = []

        """we check for matching leading characters"""
        for comm in commands:
            if len(command) <= len(comm) and command == comm[0:len(command)]:
                matches.append(comm)

        """if command is clear"""
        if(len(matches)==1):
            self.write(f"found command {matches[0]}")

            return matches[0]
        elif (len(matches)>1):
            self.write("input is ambigious, following are possible :\n")
            for match in matches:
                self.write(f" {match}")
            
            return command
        else:
            self.write(f"no matching commands found for {command}")
            return False 
```

the algorithm checks for overlapping letters in the starting indices.

so for instance if we write `me`

```
000000 [bcdimqrsw]> me
is searching command me
found command memory
IP      = 000000
R000000 = 000000
R000001 = 000000
R000002 = 000000
R000003 = 000000
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000000

 breaks 

 watchs 
```

works of course also for functions with arguments...

```
000000 [bcdimqrsw]> me 2 9
is searching command me
found command memory
  0b0302  00000a  030005  010202  020006  010204  000207  030209
```

Now if user wants to list all commands

```
000000 [bcdimqrsw]> sear
is searching command sear
found command search
 list of all commands 
d
dis
i
ip
m
memory
q
quit
r
run
s
step
b
break
c
clear
search
se
def
watch
cwatch
```

now if user wants to know if `ru` is a command ( or references a valid command)

```
000000 [bcdimqrsw]> search ru
is searching command ru
found command run
```

because sometimes we want to be sure before executing the actual command.

But what if the specified command is ambigous?

```
000001 [bcdimqrsw]> search s
is searching command s
input is ambigious, following are possible :

 s
 se
 search
 step
```

Note that if user types only `s` it will be recognized in the handlers dictionary but if using the search algorithm directly we dont check if its in the handlers dictionary. The reason for this design choice is to give programmers the ability to see all commands for a given search input.

Note that this way a help systems could be implemented which gives descriptions of the commands and examples


Lastly, the user can specify an alias to a command with `def`:

```
000001 [bcdimqrsw]> def zuuu search
alias has been successfully created zuuu is now search
000001 [bcdimqrsw]> zuuu
 list of all commands 
d
dis
i
ip
m
memory
q
quit
r
run
s
step
b
break
c
clear
search
se
def
watch
cwatch
zuuu
```

which only adds to the dictionary if it isnt already in there

```python
def define(self, alias, command):
        """
            @alias : the reference to the command
            @command : the command which shall be referenced by alias
        """
        if command not in self.handlers:
            command = self.searchComm(command)
        
        if(command == False):
            return False

        if(alias in self.handlers):
            self.write(f"{alias} is already in use!")

        value = self.handlers[command]

        self.handlers[alias] = value
        self.write(f"alias has been successfully created {alias} is now {command}")


        return True
```

### Watchpoints

We decided to implement two types of watchs via the same command, one watch for the registers since this is what assemply programmers are also interested in and watchs for memory addresses.


```python
def _do_set_watch(self,addr,args=[]):
        """
            @addr : current address the debugger is at
            @args : optional, some address to set the debugger at
            @returns : True if a berakpoint has been set
                        None if there already was a breakpoint
                        False if memory address was out of bounds
        """
        """currently code from set breakpoint"""

        if(len(args)==1):
            """store watch for register"""
            if(args[0][0] == 'R'):
                addr = args[0]
                

            else:
                addr = int(args[0])
                self.assert_is_address(addr)

        else:
            addr = int(addr)

        if addr in self.watchs:
                return
        
        if(type(addr) is str):
            self.watchs[addr] = self.reg[int(addr[1:])]
            return True
        else:
            self.watchs[addr] = self.ram[addr]
            return True

    def _do_clear_watch(self,addr,args=[]):
        """
            @addr : current address the debugger is at
            @args : optional, some address to set the debugger at
            @returns : True if a berakpoint has been cleared
                        None if there was no breakpoint
                        False if memory address was out of bounds
        """



        if(len(args)==1):

            if(args[0][0] == 'R'):
                addr = args[0]
                
            else:
                addr = int(args[0])
            

        if addr not in self.watchs:
                return
            
        del self.watchs[addr]
        return True
```

as mentionned in the introduction the watchs are checked in the run function.

just like with the `break` command one can specify a watch without argumetns, then the current ram location is taken as the memory address.

or by specifying the address

```
000005 [bcdimqrsw]> watch
000005 [bcdimqrsw]> m
IP      = 000005
R000000 = 000001
R000001 = 000005
R000002 = 000000
R000003 = 00000b
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000001

 breaks 

 watchs 
------
000005: 010202 
```

and with specified addreess

```
000005 [bcdimqrsw]> watch 7
000005 [bcdimqrsw]> m
IP      = 000005
R000000 = 000001
R000001 = 000005
R000002 = 000000
R000003 = 00000b
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000001

 breaks 

 watchs 
------
000005: 010202 
000007: 010204 
```


now we will use the following assembly code to showcase the remaining functions

```
# Count up to 3.
# - R0: loop index.
# - R1: loop limit.
ldc R0 1
ldc R1 5
ldc R3 11
loop:
prr R0
str R0 R3
ldc R2 1
add R0 R2
cpy R2 R1
sub R2 R0
bne R2 @loop
hlt

```

notice that `str R0 R3` stores the value of R0 at 11 (value of R3). Now lets watch 11.

```
000000 [bcdimqrsw]> watch 11
000000 [bcdimqrsw]> run
000001
watch triggered at 11
IP      = 000005
R000000 = 000001
R000001 = 000005
R000002 = 000000
R000003 = 00000b
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000001

 breaks 

 watchs 
------
00000b: 000000 
```

console displayes a "watch triggered" message before printing all memory, user sees the old value in the watch table and current value in the memory table.

Now we also can watch registers by simply using the watch command with a register as argument.

```
000000 [bcdimqrsw]> watch R0
000000 [bcdimqrsw]> run
watch triggered at R0
IP      = 000001
R000000 = 000001
R000001 = 000000
R000002 = 000000
R000003 = 000000
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000000

 breaks 

 watchs 
------
R0: 000000 
```

We decided to include this feature since assembly programmers are probably also interested in watching the registers.



this concludes the section for task 3 and 4
