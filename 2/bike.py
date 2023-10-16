
# example interface
class Shape:
    def __init__(self,name):
        self.name = name

    def area(self)->None:
        raise NotImplementedError("area")
    
class foo:
    def __init__(self):
        self.name = "foo"
    
class Rect(Shape,foo):
    def __init__(self, name,height,width):
        super().__init__(name)
        super().__init__
        self.height = height
        self.width = width


    def area(self)->None:
        self.area = self.heigShapeht*self.width




def square_new(name:str,sideLen:float,areaArg)->dict:
    objAttr : dict= {
        "name":name,
        "sidLen":sideLen,
        "areaCalc":0
 
    }

    objMeth :dict = {
        "area": areaArg
    }

    return {"Attr":objAttr, "Meth":objMeth}

def area2(num:float):
    return num*10

if __name__ == "__main__":
    boo = square_new("blabla",20,area2)

    boo["Meth"]["area"]
    print(boo["Attr"]["areaCalc"])




    

    

    
