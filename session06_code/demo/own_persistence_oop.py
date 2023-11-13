class SaveObjects:

    def __init__(self, writer):
        self.writer = writer
    
    def save(self, thing):
        typename = type(thing).__name__  # "bool"
        method = f"save_{typename}"  # save_bool
        # method = "save_" + typename <- same as above with less syntactic sugar
        assert hasattr(self,method), f"Unkown object type {typename}"
        m = getattr(self,method)
        m(thing)
    
    def _write(self,key,value):
        print(f"{key}:{str(value)}", file=self.writer)
    
    def save_bool(self, thing):
        self._write("bool",thing)
    
    def save_int(self, thing):
        self._write("int",thing)
    
    def save_list(self, a_list):
        length = len(a_list)
        self._write("list",length)
        for item in a_list:
            self.save(item)





#######################################
a = [10,False,2]

b = '''this is
two lines'''

with open("output_oop.txt","w") as file:
    so = SaveObjects(file)
    so.save(a)

#with open("output.txt","r") as file:
#    lo = LoadObjects(file)
#    data = lo.load(file)

#print(data)


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