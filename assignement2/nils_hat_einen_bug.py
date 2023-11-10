import sys
import json
import datetime
import random

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

# - # - # - # - #

#@log_function
def do_klasse(envs, args):
    assert len(args) == 2
    variables = args[0]  # list of variable names
    methods = args[1]  # list of method definitions
    return ["klasse", variables, methods]

#@log_function
def do_machen(envs, args):
    assert len(args) == 2
    class_name = args[0]
    instance_values = args[1]  # Assumes instance_values is a list of actual values for the class variables

    # Get the class structure from the environment
    klass = envs_get(envs, class_name)
    assert isinstance(klass, list) and klass[0] == "klasse"
    class_variables = klass[1]
    class_methods = klass[2]

    # Check if the number of instance values matches the number of class variables
    assert len(class_variables) == len(
        instance_values), "Class instantiation requires matching number of values for variables."

    # Create the instance variable structure
    instance_vars = dict(zip(class_variables, instance_values))

    # Create the instance method structure
    # Note: We create a shallow copy of each method definition to avoid mutating the class definition
    instance_methods = {method[1]: method[2] for method in class_methods}

    # Construct the instance structure
    instance_structure = ["instanz", class_name, instance_vars, instance_methods]

    return instance_structure

#@log_function
def do_ausführen(envs, args):
    # Flatten args if nested, assuming that args[0] is a list if len(args) == 1
    args = args[0] if len(args) == 1 and isinstance(args[0], list) else args
    assert len(args) >= 2, "ausführen requires 2 or more arguments"
    instance_name, method_name = args[:2]
    method_args_provided = args[2:]  # Get provided args as a list, which can be empty

    # Get the instance from the environment
    instance = envs_get(envs, instance_name)
    assert isinstance(instance, list) and instance[0] == "instanz", "First argument must be an instance name"
    _, class_name, instance_vars, instance_methods = instance

    # Get the method from the instance methods
    method = instance_methods.get(method_name)
    assert method and isinstance(method, list) and method[
        0] == "funktion", f"{method_name} is not a method of {class_name}"

    # Prepare the final arguments dictionary for the function
    final_args = {}
    provided_args_index = 0  # Keep track of which provided argument to use next

    # Iterate over the function's parameters and determine the source of each value
    for param in method[1]:  # method[1] contains the parameter names of the function
        if param in instance_vars:
            # The parameter matches an instance variable, use its value
            final_args[param] = instance_vars[param]
        elif provided_args_index < len(method_args_provided):
            # Use the next provided argument for this parameter
            final_args[param] = method_args_provided[provided_args_index]
            provided_args_index += 1
        else:
            # Not enough arguments provided
            raise AssertionError(f"Not enough arguments provided for method {method_name}")

    # Verify that all provided arguments have been used
    if provided_args_index != len(method_args_provided):
        raise AssertionError(f"Too many arguments provided for method {method_name}")

    # Create a new environment for the method call, including the instance variables as a dictionary
    envs_for_call = dict(instance_vars)  # dict() is used to ensure a copy of instance variables is passed

    list_with_abrufen = [item for pair in zip(["abrufen"] * len(envs_for_call), envs_for_call.keys()) for item in pair]
    envs_for_call[method_name] = instance_methods[method_name]
    envs.append(envs_for_call)
    result = do_aufrufen(envs, [method_name] + [list_with_abrufen])
    envs.pop()
    return result

#@log_function
def do_funktion(envs, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]

#@log_function
def do_aufrufen(envs, args):
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs, arg) for arg in arguments]

    func = envs_get(envs, name)
    assert isinstance(func, list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params, values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs, body)
    envs.pop()

    return result


def envs_get(envs, name):
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable or method name {name}"


def envs_set(envs, name, value):
    assert isinstance(name, str)
    envs[-1][name] = value

#@log_function
def do_setzen(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    envs_set(envs, var_name, value)
    return value

#@log_function
def do_abrufen(envs, args):
    assert len(args) == 1
    return envs_get(envs, args[0])

#@log_function
def do_addieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left + right

#@log_function
def do_absolutwert(envs, args):
    assert len(args) == 1
    value = do(envs, args[0])
    return abs(value)

#@log_function
def do_subtrahieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left - right

#@log_function
def do_abfolge(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result


OPERATIONS = {
    func_name.replace("do_", ""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(envs, expr):
    if isinstance(expr, int):
        return expr

    # print(expr[0])
    assert isinstance(expr, list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    res = func(envs, expr[1:])
    return res

def tester_(this, that):
    print(this + that)

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

if __name__ == "__main__":
    main()  # a python file implementing the interpreter of the LGL 2 language, as described# in the 3 exercises below;

