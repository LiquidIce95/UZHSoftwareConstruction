ldc R2 73
ldc R0 0
ldc R1 17
str R1 R2
ldc R2 42
loop:
str R1 R2
prm R2
inc R2
dec R1
bne R1 @loop
ldc R0 42
ldc R1 42
ldc R3 73
ldr R2 R3
add R1 R2
ldc R2 0
ldc R3 0
loop1:
ldr R2 R0
ldr R3 R1
swp R2 R3
str R2 R0
str R3 R1
inc R0
cpy R2 R0
cpy R3 R1
sub R3 R2
beq R3 @end
dec R1
cpy R2 R0
cpy R3 R1
sub R3 R2
end:
bne R3 @loop1
ldc R3 73
ldr R1 R3
ldc R0 0
ldc R2 42
loop2:
prm R2
inc R2
dec R1
bne R1 @loop2
prm R2
hlt
