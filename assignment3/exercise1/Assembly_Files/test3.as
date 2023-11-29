# Testing bne, prr, prm

ldc R1 2
ldc R0 1
prm R1
prr R1
add R1 R0
beq R1 2
prm R1
hlt