

ldc R2 @array_length
ldc R0 0
# modify array_length here, at least 1*********************
ldc R1 17
str R1 R2
#***********************************************

ldc R2 @array
# first loop initiating array
loop:
str R1 R2
# printing current vlaue of R2 at index R2
prm R2
inc R2
dec R1
bne R1 @loop

# end of initiation of array

# now array is initialized with values 9 to 1

# now we reverse them inplace
# pointer to start
ldc R0 @array
# pointer to end
ldc R1 @array
ldc R3 @array_length
ldr R2 R3
#now right pointer is set to end of array
add R1 R2

ldc R2 0
ldc R3 0

# reverse inplace algorithm-------------------------------
loop1:
# load value from start of array
ldr R2 R0

#laod value from end of array
ldr R3 R1

# now swap
swp R2 R3

# now load back into
str R2 R0
str R3 R1


#now increment the left pointer
inc R0

#compute diff of both poiners
cpy R2 R0
cpy R3 R1

sub R3 R2

#brach to loop if R3 equals 0 now , then pointer coincide
beq R3 @end
# check here if both coincide


# now decrement the right pointer
dec R1
#compute diff
cpy R2 R0
cpy R3 R1

sub R3 R2

#check here if both coincide

end:
# end loop if both pointers coincide
bne R3 @loop1

# end of reverse in place algorithm--------------------------

#loop through array to check


ldc R3 @array_length
ldr R1 R3
ldc R0 0
ldc R2 @array

loop2:
# printing current vlaue of R2 at index R2
prm R2
inc R2
dec R1
bne R1 @loop2
prm R2

hlt



.data
array:30
array_base: 1
array_length: 1
riterator: 1