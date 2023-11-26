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
