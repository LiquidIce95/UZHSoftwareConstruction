
class Bike:

    def __init__(self,age):
        self.age = age
        self.wheels = 2
        self.speed = 0
        self.dimension = "S"
    
    def accelerate(self,acceleration):
        self.speed = self.speed + acceleration
    
    def do_break(self):
        self.speed = 0


a_bike = Bike(12)
print(a_bike.age)

a_bike.accelerate(12)
print(f"My bike is going at this speed {a_bike.speed}")
    
