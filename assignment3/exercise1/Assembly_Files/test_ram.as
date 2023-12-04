# Testing too much RAM allocation - Allowed 256 and used 300 here.
# R0: loop index
# R1: upper limit of loop
# R2: array slot
# R3: carrier digit

ldc R0 0
ldc R1 255
ldc R2 @array
loop:
str R0 R2
ldc R3 1
add R0 R3
# Move to postion n+1 in array
add R2 R3
cpy R3 R1
# subtract R0 (1) from R3 (300)
sub R3 R0
bne R3 @loop
hlt
.data
array: 300