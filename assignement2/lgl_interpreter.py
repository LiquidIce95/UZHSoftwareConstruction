import sys
import json
import datetime
import random
import argparse

# - # - # - # - #
# Tracing functions
log = []
IDs = []
def time_stamp():
    return datetime.datetime.now()

def get_ID():
    while True:
        ID = "".join(str(random.randint(0, 9)) for _ in range(6))
        if ID not in IDs:
            IDs.append(ID)
            return ID

def log_function(func):
    ID = get_ID()
    def _inner(envs, args):
        log.append(f"{ID}, {func.__name__}, start, {time_stamp()}")
        res = func(envs, args)
        log.append(f"{ID}, {func.__name__}, stop, {time_stamp()}")
        return res
    return _inner

def push(l: list, file: str):
    with open(file, "w") as f:
        f.write("id, function_name, event, timestamp\n")
        f.write("\n".join(l))
    f.close()


def apply_decorators():
    for name in list(globals()):
        if callable(globals()[name]) and name.startswith('do_'): #and name.startswith('do_'):
            globals()[name] = log_function(globals()[name])

# - # - # - # - #

def do_klasse(envs, args):
    assert len(args) >= 2, "Wrong Format for a Klasse"
    #no parent class given
    if len(args) == 2:
        variables = args[0] 
        methods = args[1]   
        return ["klasse", None ,variables, methods]
    #parent class given
    elif len(args) == 3:
        parent = args[0]
        variables = args[1]
        methods = args[2]   
        return ["klasse", parent ,variables, methods] 
    
    assert False, "Wrong Format for a Klasse"

def do_machen(envs, args):
    assert len(args) == 2
    class_name, instance_values = args

    #retrieve the class structure from the environment.
    klass = envs_get(envs, class_name)
    assert isinstance(klass, list) and klass[0] == "klasse"

    #recursively gather class information from ancestors with the helper.
    all_variables, instance_methods = helper_gather_class_info(envs, class_name)
  
    #check if the number of instance values matches the total number of class variables.
    assert len(all_variables) == len(instance_values), \
        "Class instantiation requires matching number of values for variables."

    #create the instance variable structure.
    instance_vars = dict(zip(all_variables, instance_values))
    
    return ["instanz", class_name, instance_vars, instance_methods]

def helper_gather_class_info(envs, class_name):
    klass = envs_get(envs, class_name)
    assert klass, f"Class {class_name} not found in the environment."

    #spliting class up, "klasse" string is not need thus = _
    _, class_parent, class_variables, class_methods = klass

    #initialize variables and methods with the current class contnent.
    all_variables = class_variables.copy()
    all_methods = {method[1]: method[2] for method in class_methods}

    #recursively add parent class variables and methods.
    if class_parent is not None:
        parent_variables, parent_methods = helper_gather_class_info(envs, class_parent)
        all_variables = parent_variables + all_variables
        all_methods.update(parent_methods)

    return all_variables, all_methods

def do_ausführen(envs, args):
    #flattenargs if nested, assuming that args[0] is a list if len(args) == 1
    args = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    #args could also include aarguments for functions that do require more than just
    assert len(args) >= 2, "ausführen requires at least an instance name and a method name"
    
    instance_name, method_name = args[:2]
    method_args_provided = args[2:]  # Any additional args provided to the method call

    #retrieve the instance from envs
    instance = envs_get(envs, instance_name)
    assert isinstance(instance, list) and instance[0] == "instanz", "First argument must be an instance name"
    _, _, instance_vars, instance_methods = instance
    
    #retrieve the method to be called
    method = instance_methods.get(method_name)
    assert method and isinstance(method, list) and method[0] == "funktion", f"{method_name} is not a method of {instance_name}"

    #verify the method's required variables against instance variables and provided args
    required_vars = method[1]
    final_args = [method_name]

    for var in required_vars:
        if var in instance_vars:
            final_args.append(instance_vars[var])
        elif method_args_provided:
            final_args.append(method_args_provided.pop(0))
        else:
            assert False, f"Instance {instance_name} does not have the variable {var} and it was not provided as an argument"
    
    #check if there are leftover provided args that were not required
    if method_args_provided:
        assert False, "Too many arguments provided"

    #create a new environment for the method call, including the instance variables as a dictionary
    envs_for_call = dict(instance_vars)
    envs_for_call[method_name] = instance_methods[method_name]

    #adding the newly created env to the envs, to allow the funcitn call to work.
    envs.append(envs_for_call)
    result = do_aufrufen(envs, final_args)
    envs.pop()

    return result

def do_funktion(envs,args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion",params,body]

def do_aufrufen(envs,args):
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs,arg) for arg in arguments]

    func = envs_get(envs,name)
    assert isinstance(func,list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params,values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs,body)
    envs.pop()

    return result

def envs_get(envs, name):
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable or method name {name}"

def envs_set(envs,name,value):
    assert isinstance(name,str)
    envs[-1][name] = value
        
def do_setzen(envs,args):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    value = do(envs,args[1])
    envs_set(envs,var_name, value)
    return value

def do_abrufen(envs,args):
    assert len(args) == 1
    return envs_get(envs,args[0])

def do_addieren(envs,args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left + right

def do_subtrahieren(envs,args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left - right

'''
start Task 1, additional functionality
'''

def do_multiplizieren(envs,args):
    '''
        args[0] : left number of multiplication
        args[1] : right number
        returns : left times right
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left*right


def do_dividieren(envs,args):
    '''
        args[0] : numerator
        args[1] : denumerator
        returns : numerator / denumerator
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left / right

def do_potenzieren(envs,args):
    '''
        args[0] : basis of power
        args[1] : exponent
        returns : basis^exponent
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left**right

def do_kleinergl(envs,args):
    '''
        args[0] : a
        args[1] : b
        returns : int(a < b or a == b)
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    assert isinstance(left,int,float) and isinstance(right,int,float)
    return int(left <= right)

def do_kleiner(envs,args):
    '''
        args[0] : a
        args[0] : b
        returns : int(a < b)
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    assert isinstance(left,int) and isinstance(right,int)
    return int(left < right)

def do_gleich(envs,args):
    '''
        args[0] : a
        args[1] : b
        returns : int(a==b)
    '''
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return int(left == right)

def do_und(envs,args):
    '''
        args[0] : a
        args[1] : b
        returns : int(bool(a) and bool(b))
    '''
    assert len(args) == 2
    left = bool(do(envs,args[0]))
    right = bool(do(envs,args[1]))
    return int(left and right)

def do_oder(envs,args):
    '''
        args[0] : a
        args[1] : b
        returns : int(bool(a) or bool(b))
    '''
    assert len(args) == 2
    left = bool(do(envs,args[0]))
    right = bool(do(envs,args[1]))
    return int(left or right)


def do_drucken(envs,args):
    '''
        args[0] : value to be printed
        yields : print of value onto console
    '''
    assert len(args)==1
    res = do(envs,args[0])
    print(f"=> {res}")

def do_solange(envs,args):
    '''
        args[0] : condition to be checked on each
        iteratoin
        args[1] : commands to be executed on each iteration
        as long as condition is true
        returns : the conditions in the final state
    '''
    assert len(args) == 2
    
    while(do(envs,args[0])):
        do(envs,args[1])

    return do(envs,args[0])


def do_liste(envs,args):
    '''
        args[0] : name of list
        args[1:]: values to be store in list
        returns : the list with all values
    '''
    assert len(args) > 0
    liste = []
    for arg in args[1:]:
        liste.append(do(envs,arg))

    envs_set(envs,args[0], liste)
    return liste


def do_schauen(envs,args):
    '''
        args[0] : list object
        args[1] : the index
        returns : list[index]
    '''
    assert len(args) == 2
    liste = do(envs,args[0])
    index = do(envs,args[1])
    assert isinstance(liste,list)
    assert isinstance(index,int)
    assert 0 <= index and index < len(liste)

    return liste[index]


def do_lsetzen(envs,args):
    ''' args[0] list object
        args[1] index
        args[2] value to set at index
    '''
    assert len(args) == 3
    liste = do(envs,args[0])
    index = do(envs,args[1])
    value = do(envs,args[2])
    assert isinstance(liste,list)
    assert isinstance(index,int)
    assert 0 <= index and index < len(liste)

    liste[index] = value
    return value

def do_llaenge(envs,args):
    '''
        args[0] : list object
        returns : length of list
    '''
    assert len(args[0]) == 1
    lis = do(envs,args[0])
    assert isinstance(lis,list)

    return len(lis)

def do_Wbuch(envs,args):
    '''
        args[0] : name of dictionary
        args[1:]: (key,value) pairs
        returns : the dictionarey with each key,value pair
    '''
    assert len(args) >0
    dict = {}
    for arg in args[1:]:
        assert len(arg)==2
        dict[do(envs,arg[0])]=do(envs,arg[1])

    envs_set(envs,args[0], dict)
    return dict

def do_Wschauen(envs,args):
    '''
        args[0] : dictionary object
        args[1] : key which is in dictionary
        returns : the value corresponding to key
    '''
    assert len(args)==2
    dic = do(envs,args[0])
    key = do(envs,args[1])

    assert isinstance(dic,dict)
    assert key in dic

    return dic[key]

def do_Wsetzen(envs,args):
    '''
        args[0] : dictionary object
        args[1] : key in dictionary
        args[2] : value to be set at key
        returns : the modified dictionary
    '''
    assert len(args) == 3
    dic = do(envs,args[0])
    assert isinstance(dic,dict)

    key = do(envs,args[1])

    value = do(envs,args[2])
    dic[key] = value
    return dic

def is_iterable(obj):
    '''
        obj: the object to check
        returns : true if obj is an iterable
    '''
    try:
        iter(obj)
        return True
    except TypeError:
        return False
    

def do_istdrin(envs,args):
    '''
        args[0] : iterable object A
        args[1] : object B to check membership of A
        returns : B in A
    '''
    assert len(args)==2
    ite = do(envs,args[0])
    obj = do(envs,args[1])
    assert is_iterable(ite)

    return int(obj in ite)

def do_mischen(envs,args):
    '''
        args[0] : list object A
        args[1] : list object B
        returns : A | B , python function
    '''
    assert len(args) == 3
    dic1 = do(envs,args[1])
    dic2 = do(envs,args[2])

    assert isinstance(dic1,dict)
    assert isinstance(dic2,dict)

    dic3 = dic1 | dic2

    envs_set(envs,args[0], dic3)
    return dic3


def do_wennDann(envs,args):
    '''
        args[0] : condition to ve evalueated
        args[1] : instruction to execute if condition is true
        returns : the condition after evaluation if the condition was false
        otherwise if the condition was successfull it returns the result of the 
        operation executed
    '''

    assert len(args)==2

    cond = do(envs,args[0])

    if(bool(cond)):
        return do(envs,args[1])
    
    return cond
'''
end Task 1, additional functionality
'''

def do_abfolge(envs,args):
    assert len(args) > 0
    for operation in args:
        result = do(envs,operation)
    return result

def do(envs,expr):
    if isinstance(expr,int) or isinstance(expr, float):
        return expr

    #print(expr[0])
    assert isinstance(expr,list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    res = func(envs, expr[1:])
    return res

def main():
    assert len(sys.argv) >= 2, "Usage: funcs-demo.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)

    # Variables for Tracing
    tracing = False
    # Tracing on/off
    for i, el in enumerate(sys.argv):
        if el == "--trace":
            tracing = True
            file = sys.argv[i + 1]
            
    # Output vo dem isch:
    # <function do_setzen at 0x1037a1080>
    # <function log_function at 0x102fe34c0>


    if tracing:
        for key, val in globals().items():
            if key.startswith("do_"):
                globals()[key] = log_function(val)

    # Output vo dem isch:
    # <function log_function.<locals>._inner at 0x1037a1940> --> demfall hets die änderig nur lokal überno? Wie mach ichs demfall global?
    # <function log_function at 0x102fe34c0>

    envs = [{}]
    result = do(envs, program)
    print(f"=> {result}")

    if tracing:
        push(log, file)

apply_decorators()

OPERATIONS = {
    func_name.replace("do_",""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


if __name__ == "__main__":
    main()# a python file implementing the interpreter of the LGL 2 language, as described# in the 3 exercises below;
