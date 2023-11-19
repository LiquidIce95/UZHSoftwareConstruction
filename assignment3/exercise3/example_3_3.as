
# - R0: loop index.
# - R1: loop limit.
# - R2: array index/address.
# - R3: temporary.


ldc R0 0
ldc R1 10

ldc R2 @array


loop:
dec R1
str R1 R2
# printing current vlaue of R2 at index R2
ldr R3 R2
str R3 R2
prr R3
inc R2
bne R1 @loop




# now array is initialized with values 9 to 0

# now we reverse them inplace
# pointer to start
ldc R0 @array
# pointer to end
ldc R1 @array
ldc R2 10
add R1 R2

ldc R2 0
ldc R3 0


loop1:
# load value from end of array
ldr R2 R0

#laod value from start of array
ldr R3 R1

# now swap
swp R2 R3

# now load back into
str R2 R0
str R3 R1

#now increment the left pointer
inc R0
dec R1

#compute diff of both poiners
cpy R2 R0
cpy R3 R1

sub R3 R2
# end loop if both pointers coincide
bne R3 @loop1



#loop through array to check

ldc R0 0
ldc R1 10
ldc R2 @array

prr R1
prr R0
prr R0
prr R1

loop2:
dec R1

# printing current vlaue of R2 at index R2
ldr R3 R2
prr R3
inc R2
bne R1 @loop2

hlt


.data
array:10
array_base: 1
array_length: 1