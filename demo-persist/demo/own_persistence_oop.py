class SaveObjects:

    def __init__(self, writer):
        self.writer = writer
    
    def save(self, thing):
        typename = type(thing).__name__  # "list"
        method = f"save_{typename}"  # save_list
        # method = "save_" + typename <- same as above with less syntactic sugar
        assert hasattr(self,method), f"Unkown object type {typename}"
        m = getattr(self,method)
        m(thing)
    
    def _write(self,*fields):
        print(":".join(str(f) for f in fields), file=self.writer)
    
    def save_bool(self, thing):
        self._write("bool",thing)
    
    def save_float(self, thing):
        assert isinstance(thing,float), f"{thing} is not a float"
        self._write("float",thing)
    
    def save_int(self, thing):
        self._write("int",thing)
    
    def save_list(self, a_list):
        length = len(a_list)
        self._write("list",length)
        for item in a_list:
            self.save(item)
    
    def save_dict(self, a_dict):
        length = len(a_dict)
        self._write("dict",length)
        temp_list = [item for pair in a_dict.items() for item in pair]
        for item in temp_list:
            self.save(item)


class LoadObjects:

    def __init__(self, reader):
        self.reader = reader
    
    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read, sorry"
        fields = line.split(":")
        assert len(fields) == 2, f"Badly formatted line {line}"

        key, value = fields
        method = f"load_{key}"
        assert hasattr(self,method), f"Unkown object type {key}"
        m = getattr(self,method)
        return m(value)
    
    def load_bool(self, value):
        return value == "True"
    
    def load_int(self,value):
        return int(value)
    
    def load_list(self,value):
        l = []
        for element in range(int(value)):
            l.append(self.load())
        return l





#######################################
# a = [10,False,2]

# b = '''this is
# two lines'''

# c = {1:False, 2:10}

# d = [1,2]

# e = [10,d,d]

# with open("output_oop.txt","w") as file:
#     so = SaveObjects(file)
#     so.save(e)

# with open("output_oop.txt","r") as file:
#     lo = LoadObjects(file)
#     data = lo.load()

# print(data)


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