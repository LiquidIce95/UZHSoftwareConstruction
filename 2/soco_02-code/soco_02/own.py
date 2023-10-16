def shape_density(instance, weight):
    area = call(instance,"area")
    return weight / area

def shape_hurra(instance):
    return "hurra!"

def shape_perimeter(instance):
    raise NotImplementedError("Perimeter")

Shape = {
    "density":shape_density,
    "hurra":shape_hurra,
    "perimeter":shape_perimeter,
    "_classname":"Shape",
    "_parent":None
}




############## SQUARE #################
def square_perimeter(instance):
    return 4 * instance["side_length"]

def square_area(instance):
    return instance["side_length"] ** 2

def square_diagonal(instance):
    return instance["side_length"] ** 0.5

def square_larger(instance,another_side_length):
    return another_side_length > instance['side_length']

Square = {
    "perimeter":square_perimeter,
    "area":square_area,
    "larger":square_larger,
    "_classname":"Square",
    "_parent": Shape
}

def square_new(name,side_length):
    square_obj = {
        "name":name, #attribute
        "side_length":side_length, #attribute
        "_class":Square
    }
    return square_obj

############## CIRCLE #################
def circle_perimeter(instance):
    return instance['radius_length'] * 2 * 3.14

def circle_area(instance):
    return instance['radius_length'] ** 2 * 3.14

def circle_larger(instance,another_radius_length):
    return another_radius_length > instance['radius_length']

Circle = {
    #"perimeter":circle_perimeter,
    "area":circle_area,
    "larger":circle_larger,
    "_classname":"Circle",
    "_parent": Shape
}

def circle_new(name,radius_length):
    circle_obj = {
        "name":name, #attribute/data
        "radius_length":radius_length, #attribute/data
        "_class":Circle
    }
    return circle_obj


########### HELPER FUNCTION #############
def call(instance,method_name,*args):
    method = find(instance["_class"], method_name)
    return method(instance,*args)

def find(cls,method_name):
    if method_name in cls:
        return cls[method_name]
    else:
        if cls["_parent"] == None:
            raise NotImplementedError(f" {method_name} is not implemented")
        else:
            return find(cls["_parent"],method_name)


########### MAIN EXECUTION #############

elements = [square_new("sq",3),circle_new("ci",2)]
for el in elements:
    n = el["name"]
    p = call(el,"perimeter")
    a = call(el,"area")
    l = call(el,"larger",10)
    d = call(el,"density",10)
    h = call(el,"hurra")
    print(f"Shape {n}: perimeter: {p}, area: {a}")
    print(f"Is it larger? {l}")
    print(f"density is {d}")
    print(h)