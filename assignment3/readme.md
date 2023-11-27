

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

to prove the correctness of the algorithm we refer to the comments of the algorithm in example_3_3.as file

first Invariant:

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


One Major change despite moving everything into one file is the interact function:

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

here we first check if an address is being watched. We first tried to implement the watch just like breaks but that made it impossible to check if the value has changed (since the value at that address is a watch and not the original value anymore). Its for sure not the moste efficient solution. But considering time constraints of development, decreasing development time seemed to be more important.




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

Note that if user types only `s` it will be recognized in the handlers dictionary but if using the search algorithm directly we dont check if its in the handlers dictionary.


Lastly, the user can specify and alias to a command with `def`:

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
        if command not in self.handlers:
            command = self.searchComm(command)
        
        if(command == False):
            return False

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
000004 [bcdimqrswz]> watch
000004 [bcdimqrswz]> m
IP      = 000004
R000000 = 000001
R000001 = 000005
R000002 = 000000
R000003 = 00000b
000000:   010002  050102  0b0302  00000a
000004:   030005  010202  020006  010204
000008:   000207  030209  000001  000000

 breaks 

 watchs 
------
000004: 196613 
```

and below in teh watchs section our created watch is printed



