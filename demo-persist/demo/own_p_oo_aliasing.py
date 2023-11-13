from typing import Any
from own_persistence_oop import SaveObjects
from own_persistence_oop import LoadObjects

class SaveAlias(SaveObjects):

    def __init__(self, writer):
        super().__init__(writer)
        self.seen = set()
    
    def save(self, thing):
        thing_id = id(thing)
        if thing_id in self.seen:
            self._write("alias", thing_id, "")
            return
        
        self.seen.add(thing_id)
        typename = type(thing).__name__  # "list"
        method = f"_{typename}"  # save_list
        # method = "save_" + typename <- same as above with less syntactic sugar
        assert hasattr(self,method), f"Unkown object type {typename}"
        m = getattr(self,method)
        m(thing)
    
    def _bool(self, value):
        self._write("bool",id(value),value)
    
    def _int(self, value):
        self._write("int",id(value),value)
    
    def _list(self, a_list):
        length = len(a_list)
        self._write("list",id(a_list),length)
        for item in a_list:
            self.save(item)
    
class LoadAlias(LoadObjects):

    def __init__(self, reader):
        super().__init__(reader)
        self.seen = {}

    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "Nothing to read, sorry"
        fields = line.split(":")
        assert len(fields) == 3, f"Badly formatted line {line}"
        key, ident, value = fields

        if key == "alias":
            assert ident in self.seen
            return self.seen[ident]

        method = f"load_{key}"
        assert hasattr(self,method), f"Unkown object type {key}"
        m = getattr(self,method)
        result = m(value)
        self.seen[ident] = result
        return result





#####
a = 10
b = 11

l = [a,a,b]

with open("output_oop_alias.txt","w") as file:
    so = SaveAlias(file)
    so.save(l)


with open("output_oop_alias.txt","r") as file:
    lo = LoadAlias(file)
    data = lo.load()

print(data)
for e in data:
    print(id(e))