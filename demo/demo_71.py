import struct

# fmt = "ii"  # two 32-bit integers
# x = 31
# y = 65

# binary = struct.pack(fmt,x,y)
# print("binary representation:", binary)

# with open("test.bin","wb") as f:
#     f.write(binary)

# with open("test.txt","w") as f:
#     f.write("313 365")


# v1,v2 = struct.unpack(fmt, binary)
# print("back to normal: ", v1, v2)


#print(struct.pack("3i", 1, 2, 3))
#print(struct.pack("5s", bytes("hällo","utf-8")))
#print(struct.pack("5s", bytes("a longer string","utf-8")))


fmt = "3i"
packed = struct.pack(fmt, 1, 2, 3)

unpacked = struct.unpack(fmt,packed)
print(unpacked)

fmt = "5s"
packed = struct.pack(fmt, bytes("hallo","utf-8"))
unpacked = struct.unpack(fmt,packed)
print(unpacked)

#text = "hello world"
#print(f"{len(text)}")

#print(struct.pack(f"{len(text)}s", bytes(text,"utf-8")))

