
def save(writer,thing):
    if isinstance(thing, bool):
        print(f"bool:{thing}", file=writer)
    
    elif isinstance(thing, float):
        print(f"float:{thing}", file=writer)
    
    elif isinstance(thing,int):
        print(f"int:{thing}", file=writer)
    
    elif isinstance(thing,str):
        lines = thing.split('\n')
        length = len(lines)
        print(f"str:{length}", file=writer)
        for line in lines:
            print(line,file=writer)
        
    elif isinstance(thing,list):
        length = len(thing)
        print(f"list:{length}",file=writer)
        for item in thing:
            save(writer,item)

    else:
        raise ValueError(f"unknown type for thing {type(thing)}")

#######################################


def load(reader):
    line = reader.readline()[:-1]
    assert line, "Nothing to read, sorry"
    fields = line.split(":")
    assert len(fields) == 2, f"Badly formatted line {line}"
    key, value = fields

    if key == "bool":
        names = {"True":True, "False":False}
        assert value in names, f"Unknown Boolean {value}"
        return names[value]
    
    elif key == "float":
        return float(value)
    elif key == "int":
        return int(value)
    elif key == "str":
        num_lines = int(value)
        my_string = ""
        for i in range(num_lines):
           my_string += reader.readline()
        return my_string[:-1]
    elif key == "list":
        length = int(value)
        l = []
        for i in range(length):
           l.append(load(reader))
        return l

    else:
       raise ValueError(f"unknown type for {key}:{value}") 




#######################################
a = ["1",False,3]

b = '''this is
two lines'''

with open("output.txt","w") as file:
    save(file,a)

with open("output.txt","r") as file:
    data = load(file)

print(data)


# given a python data point like
# False

# example output
# bool:False

# given a python data point like
# 1.2

# example output
# float:1.2

# string in python
# '''hello world,
# how are you?'''

# example output
# str:2
# hello world,
# how are you?

# list in python
# [1,2]

# example output
# list:2
# int:1
# int:2