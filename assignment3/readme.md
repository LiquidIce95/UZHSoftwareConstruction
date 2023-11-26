

## Task 3

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

at teh ldc R1 17 instruction, note that the algorithm assumes length to be at least 1 since for 0 the array is empty and there are no elements to reverse 

## Task 4

Since Greg admitted in the lecture that his architecture makes no sense and was designed that way only for educational purposes, we decided to design only one debugger class **VirtaulMachineBase** in which all functionality is in. Furthermore we made sure to keep all functions small in size and never more than 3 nested (3 identation levels deep) although there are few excpetions. We also kept the handlers dictionaray and strucutre with the "_do_" functions.



### Show Memory Range





### Breakpoint Addresses


### Command Completion


### Watchpoints