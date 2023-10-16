def first():
    print("First")

def second():
    print("Second")

def third():
    print("Third")


l = [first,second,third]
for f in l:
    f()

