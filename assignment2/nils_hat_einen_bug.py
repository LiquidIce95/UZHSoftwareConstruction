import sys
import json
import datetime
import random
import argparse

# - # - # - # - #
# Tracing functions
log = []
def time_stamp():
    return datetime.datetime.now()

def get_ID():
    ID = ""
    for i in range(0, 6):
        ID += str(random.randint(0, 9))
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
    assert len(args) >= 2
    if len(args) == 2:
        variables = args[0]  # list of variable names
        methods = args[1]    # list of method definitions
        return ["klasse", None ,variables, methods]
    elif len(args) == 3:
        parent = args[0]
        variables = args[1]  # list of variable names
        methods = args[2]    # list of method definitions
        return ["klasse", parent ,variables, methods] 
    
    assert False, "Wrong Format for a Klasse"

def do_machen(envs, args):
    # This function now takes a variable 'total_vars_needed' to keep track of the number of variables needed.
    assert len(args) == 2
    class_name, instance_values = args

    # Retrieve the class structure from the environment.
    klass = envs_get(envs, class_name)
    assert isinstance(klass, list) and klass[0] == "klasse"

    # Recursively gather class information from ancestors.
    all_variables, all_methods = helper_gather_class_info(envs, class_name)

    # Check if the number of instance values matches the total number of class variables.
    assert len(all_variables) == len(instance_values), \
        "Class instantiation requires matching number of values for variables."

    # Create the instance variable structure.
    instance_vars = dict(zip(all_variables, instance_values))

    # Create the instance method structure, making sure to copy methods to avoid mutation.
    instance_methods = {method_name: method for method_name, method in all_methods.items()}

    # Construct the instance structure.
    instance_structure = ["instanz", class_name, instance_vars, instance_methods]
    
    return instance_structure

def helper_gather_class_info(envs, class_name):

    klass = envs_get(envs, class_name)
    if not klass:  # If class not found, raise an error or return a default value.
        raise ValueError(f"Class {class_name} not found in the environment.")

    _, class_parent, class_variables, class_methods = klass

    # Initialize variables and methods with the current class's definitions.
    all_variables = class_variables.copy()
    all_methods = {method[1]: method[2] for method in class_methods}

    # Recursively add parent class variables and methods.
    if class_parent is not None:
        parent_variables, parent_methods = helper_gather_class_info(envs, class_parent)
        all_variables = parent_variables + all_variables  # Parent vars come first.
        all_methods.update(parent_methods)  # Parent methods are updated (or added if new).

    return all_variables, all_methods

def do_ausführen(envs, args):
    # Flatten args if nested, assuming that args[0] is a list if len(args) == 1
    args = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    assert len(args) >= 2, "ausführen requires at least an instance name and a method name"
    
    instance_name, method_name = args[:2]
    method_args_provided = args[2:]  # Any additional args provided to the method call

    # Retrieve the instance from envs
    instance = envs_get(envs, instance_name)
    assert isinstance(instance, list) and instance[0] == "instanz", "First argument must be an instance name"
    _, class_name, instance_vars, instance_methods = instance
    
    # Retrieve the method to be called
    method = instance_methods.get(method_name)
    assert method and isinstance(method, list) and method[0] == "funktion", f"{method_name} is not a method of {instance_name}"

    # Verify the method's required variables against instance variables and provided args
    required_vars = method[1]
    final_args = [method_name]  # Start the call_me_baby list with the method name

    for var in required_vars:
        if var in instance_vars:
            final_args.append(instance_vars[var])
        elif method_args_provided:
            final_args.append(method_args_provided.pop(0))
        else:
            raise AssertionError(f"Instance {instance_name} does not have the variable {var} and it was not provided as an argument")
    
    # Check if there are leftover provided args that were not required
    if method_args_provided:
        raise AssertionError(f"Too many arguments provided: {method_args_provided}")

    # Create a new environment for the method call, including the instance variables as a dictionary
    envs_for_call = dict(instance_vars)  # dict() is used to ensure a copy of instance variables is passed
    args_for_func = [key for key in envs_for_call.values()] # old line if stuff goes south: list_with_abrufen = [item for pair in zip(["abrufen"]*len(envs_for_call), envs_for_call.keys()) for item in pair]
    envs_for_call[method_name] = instance_methods[method_name]
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

def do_addieren2(envs,args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs,args[1])
    return left * right


def do_abfolge(envs,args):
    assert len(args) > 0
    for operation in args:
        result = do(envs,operation)
    return result

def do(envs,expr):
    if isinstance(expr,int):
        return expr

    #print(expr[0])
    assert isinstance(expr,list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    res = func(envs, expr[1:])
    return res

def do_do():
    a = 2
    return None

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

    print(globals()["do_setzen"])
    print(globals()["log_function"])
    # Output vo dem isch:
    # <function do_setzen at 0x1037a1080>
    # <function log_function at 0x102fe34c0>


    if tracing:
        for key, val in globals().items():
            if key.startswith("do_"):
                globals()[key] = log_function(val)

    print(globals()["do_setzen"])
    print(globals()["log_function"])
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
    main()

