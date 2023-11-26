
# - R0: loop index.
# - R1: loop limit.
# - R2: array index/address.
# - R3: temporary.

ldc R2 @array_length
ldc R0 0
# modify array_length here
ldc R1 9
str R1 R2

ldc R2 @array

# first loop initiating array
loop:
str R1 R2
# printing current vlaue of R2 at index R2
prm R2
inc R2
dec R1
bne R1 @loop



# now array is initialized with values 9 to 1

# now we reverse them inplace
# pointer to start
ldc R0 @array
# pointer to end
ldc R1 @array
ldc R2 8
add R1 R2

ldc R2 0
ldc R3 0

# reverse inplace algorithm------------
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



#loop through array to check


ldc R2 @array_length
ldc R0 0
# modify array_length here
ldc R1 9
ldc R2 @array

# first loop initiating array
loop2:
# printing current vlaue of R2 at index R2
prm R2
inc R2
dec R1
bne R1 @loop2

hlt


.data
array:9
array_base: 1
array_length: 1
riterator: 1