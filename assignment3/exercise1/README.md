# Exercise 1: Unit Testing 
## Implementation
You are requested to write unit tests for the Assembler and the Virtual Machine implemented in [Chapter 25](https://third-bit.com/sdxpy/vm/)
and [Chapter 26](https://third-bit.com/sdxpy/debugger/) 
respectively. You will do this by using **pytest** which is a popular, simple yet powerful testing framework for the Python 
language.

### A To test the Assembler:
- write simple assembly programs of your choice (.as files);
- manually calculate the output VM instructions for each input assembly program;
- run the assembly programs through the Assembler to produce one .mx file for each .as file; (iv) compare the output of the Assembler to what you calculated in step (ii).
### To test the Virtual Machine:
- assume that the Assembler is correct (how much more complicated would things be without this assumption?);
- run the .mx files you produced in step (A)(iii) above through the VM;
- compare the output of the VM with the expected output of each program you chose in step
(A)(i).
### In (B) you tested the VM from a machine code perspective. Here, you will also test 2 common errors that occur during software development:
- Out-of-memory error; since our VM only has a finite amount of RAM, it is expected that if a user requests to allocate space for an array that exceeds this amount, the program should crash. Write a test case for this scenario.
- Instruction-not-found error; write a test case for the scenario where a given .mx file contains a code that corresponds to unknown instruction.
### Measure and report the test coverage in % for the above tests.
[Source](https://medium.com/@sumanrbt1997/code-coverage-with-pytest-1f72653b0bf2) Whichever syntax you choose for measuring line coverage, 
describe it in the README.md file for reproducibility.

**Cover all 11 Instructions.**

Place your file(s) in the exercise 1/ subfolder (see Figure 1). The pytest framework allows for a certain degree of freedom in the directory and file structure, so the only requirement here is that when you run the terminal command
```pytest``` All the Tests from this folder should run.