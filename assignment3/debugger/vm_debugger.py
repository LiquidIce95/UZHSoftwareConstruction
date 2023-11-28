import sys

from architecture import NUM_REG, OP_MASK, OP_SHIFT, OPS, RAM_LEN, VMState

COLUMNS = 4
DIGITS = 8
OPS_LOOKUP = {value["code"]: key for key, value in OPS.items()}

class VirtualMachineBase:
    @classmethod
    def main(cls):
        """Run a program and show the result."""
        assert len(sys.argv) == 2, f"Usage: {sys.argv[0]} program"
        with open(sys.argv[1], "r") as reader:
            lines = [ln.strip() for ln in reader.readlines()]
        program = [int(ln, 16) for ln in lines if ln]
        vm = cls()
        vm.initialize(program)
        vm.run()
        vm.show()

    # [init]
    def __init__(self, reader=input,writer=sys.stdout):
        """Set up memory."""
        self.writer = writer
        self.initialize([])
        """imported from vm_step.py"""
        self.reader = reader
        self.breaks = {}

        self.watchs = {}

        """imported from vm_extend.py"""
        self.handlers = {
            "d": self._do_disassemble,
            "dis": self._do_disassemble,
            "i": self._do_ip,
            "ip": self._do_ip,
            "m": self._do_memory,
            "memory": self._do_memory,
            "q": self._do_quit,
            "quit": self._do_quit,
            "r": self._do_run,
            "run": self._do_run,
            "s": self._do_step,
            "step": self._do_step,
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
            "search": self._do_search_command,
            "se": self._do_search_command,
            "def": self._do_define,
            "watch" : self._do_set_watch,
            "cwatch" : self._do_clear_watch
        }


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
        

    # [/init]

    def initialize(self, program):
        """Copy the program into memory and clear everything else."""
        assert len(program) <= RAM_LEN, "Program is too long for memory"
        self.ram = [program[i] if (i < len(program)) else 0 for i in range(RAM_LEN)]
        self.ip = 0
        self.reg = [0] * NUM_REG

    # [run]
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
    # [/run]

    def fetch(self):
        """Get the next instruction."""
        assert (
            0 <= self.ip < len(self.ram)
        ), f"Program counter {self.ip:06x} out of range 0..{len(self.ram):06x}"
        old_ip = self.ip
        instruction = self.ram[self.ip]
        self.ip += 1
        return (old_ip, *self.decode(instruction))

    def decode(self, instruction):
        """Decode an instruction to get an op code and its operands."""
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return op, arg0, arg1

    def execute(self, op, arg0, arg1):
        """Execute a single instruction."""
        if op == OPS["hlt"]["code"]:
            self.state = VMState.FINISHED

        elif op == OPS["ldc"]["code"]:
            self.assert_is_register(arg0)
            self.reg[arg0] = arg1

        elif op == OPS["ldr"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] = self.ram[self.reg[arg1]]

        elif op == OPS["cpy"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] = self.reg[arg1]

        elif op == OPS["str"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.assert_is_address(self.reg[arg1])
            self.ram[self.reg[arg1]] = self.reg[arg0]

        elif op == OPS["add"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] += self.reg[arg1]

        elif op == OPS["sub"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] -= self.reg[arg1]

        elif op == OPS["beq"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(arg1)
            if self.reg[arg0] == 0:
                self.ip = arg1

        elif op == OPS["bne"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(arg1)
            if self.reg[arg0] != 0:
                self.ip = arg1

        # [prr]
        elif op == OPS["prr"]["code"]:
            self.assert_is_register(arg0)
            self.write(f"{self.reg[arg0]:06x}")
        # [/prr]

        elif op == OPS["prm"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(self.reg[arg0])
            self.write(f"{self.ram[self.reg[arg0]]:06x}")

        else:
            assert False, f"Unknown op {op:06x}"

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

    def show(self,args=[]):
        """
            @args : list of optional argument 
                    first one being first memory address
                    second one being second memory address
            @yields: if no memory address is provided then all memory is printed (previous version)
                     if one memory address is provided then value of that address is printed
                     if two addresses are provided then all memory between is printed
        """
        """Show the IP, registers, and memory."""
        """ task4: we want to preserve the basic function, if no arguments are 
            provided then all memory is shown
        """

        """feedback to user if args make no sense"""
        
        base = 0
        top = 0
        

        if(len(args)>2):
            self.write("too many arguments provided only 1 or 2 possible")
            return None

        elif (0<len(args)<=2):
            self.showBetweenMemo(args)

        else:
            """proceed with max memory range"""
            top = max(i for (i, m) in enumerate(self.ram) if m != 0)

            base = int(base)
            top = int(top)

            self.assert_is_address(base)
            self.assert_is_address(top)

            # Show IP and registers
            self.write(f"IP{' ' * 6}= {self.ip:06x}")
            for (i, r) in enumerate(self.reg):
                self.write(f"R{i:06x} = {r:06x}")

            # How much memory to show

            # Show memory
            while base <= top:
                output = f"{base:06x}: "
                for i in range(COLUMNS):
                    output += f"  {self.ram[base + i]:06x}"
                self.write(output)
                base += COLUMNS
                

            """copied from vm_break.py"""
            self.write("\n breaks \b")
            if self.breaks:
                self.write("-" * 6)
                for key, instruction in self.breaks.items():
                    self.write(f"{key:06x}: {self.disassemble(key, instruction)}")

            self.write("\n watchs \b")
            if self.watchs:
                self.write("-" * 6)
                for key, value in self.watchs.items():
                    value = int(value)
                    if(type(key) is int):
                        self.write(f"{key:06x}: {value:06x} ")  
                    else:
                        self.write(f"{key}: {value:06x} ")  

    def assert_is_register(self, reg):
        assert 0 <= reg < len(self.reg), f"Invalid register {reg:06x}"

    def assert_is_address(self, addr):
        assert 0 <= addr < len(self.ram), f"Invalid register {addr:06x}"

    # [write]
    def write(self, *args):
        msg = "".join(args) + "\n"
        self.writer.write(msg)
    # [/write]

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


    def disassemble(self, addr, instruction):
        """
        copied from vm_step.py
        """
        op, arg0, arg1 = self.decode(instruction)
        assert op in OPS_LOOKUP, f"Unknown op code {op} at {addr}"
        return f"{OPS_LOOKUP[op]} | {arg0} | {arg1}"
    # [/disassemble]

    # [read]
    def read(self, prompt):
        """
        copied from vm_step.py
        """
        return self.reader(prompt).strip()
    
    """ INVARIANT: all do_ functions below must have as arguments: self, addr , if necessary also self, addr and args
        args is a list with arguments if do_ function can be called with or without args, 
        make a default value args=[]
    """
    def _do_disassemble(self, addr):
        """copied from vm_extend.py"""

        self.write(self.disassemble(addr, self.ram[addr]))
        return True

    def _do_ip(self, addr, args):
        """copied from vm_extend.py"""     

        self.write(f"{self.ip:06x}")
        return True

    # [memory]
    def _do_memory(self,addr,args=[]):
        """copied from vm_extend.py"""  

        self.show(args)
        return True
    # [/memory]

    def _do_quit(self, addr):
        """copied from vm_extend.py"""

        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        """copied from vm_extend.py"""

        self.state = VMState.RUNNING
        return False

    # [step]
    def _do_step(self, addr):
        """copied from vm_extend.py"""

        self.state = VMState.STEPPING
        return False
    # [/step]

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
    # [/add]

    # [clear]
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
        
    def _do_search_command(self,addr,args=[]):
        self.searchComm(args)

        return True

    def _do_define(self,addr,args=[]):
        """
            solves ex 4.3
            @args : arg[0] is the alias arg[1] is the command
            @returns True if alias was successfull created None otherwise 
        """
        if(len(args)!=2):
            self.write("you need to specify exactly two args")
            return None
        
        result = self.define(args[0],args[1])

        if (result == True):
            return True
        else:
            return None

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


if __name__ == "__main__":
    VirtualMachineBase.main()
