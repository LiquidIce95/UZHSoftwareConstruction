class Shape:
    def __init__(self,name):
        self.name = name
    
    def perimeter(self):
        raise NotImplementedError("Perimeter")
    
    def area(self):
        raise NotImplementedError("Area")
    
    def density(self, weight):
        return weight / self.area()


class Square(Shape):
    def __init__(self,name,side_length):
        super().__init__(name)
        self.side_length = side_length
    
    def perimeter(self):
        return 4 * self.side_length
    
    def area(self):
        return self.side_length ** 2
    
    def diagonal(self):
        return self.side_length ** 0.5


class Circle(Shape):
    def __init__(self,name,radius_length):
        super().__init__(name)
        self.radius_length = radius_length
    
    def perimeter(self):
        return 2 * self.radius_length * 3.14
    
    def area(self):
        return self.radius_length ** 2 * 3.14


elements = [Square("sq",3),Circle("ci",2)]
for el in elements:
    n = el.name
    p = el.perimeter()
    a = el.area()
    d = el.density(123)
    print(f"Shape {n}: perimeter: {p}, area: {a}, density: {d}")
