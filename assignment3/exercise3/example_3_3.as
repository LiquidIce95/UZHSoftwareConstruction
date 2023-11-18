
ldr R0 @array_base
ldc R1 @array_length

# customize here length of array and actual content
# for demonstration we use 10 as length
ldc R2 10

# set the actual length to 10
add R1 R2

# set loop limit
ldc R3 10
# set the 'iterator' to base address
ldr R4 R0

loop:
# store value to array
ldc R4 R3

# increment the loop iterator
inc R4
# decrement the loop limit
dec R3 
bne R3 @loop

# now array is initialized with values 10 to 1


# now we reverse them inplace


hlt


.data
array_base: 1
array_length: 1