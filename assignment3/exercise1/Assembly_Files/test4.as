# Testing bne, prr
# Counts from 3 backwards

ldc R0 3
ldc R1 1
prr R0
sub R0 R1
bne R0 1
prr R0
hlt