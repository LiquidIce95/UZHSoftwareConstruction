import sys
import json

def do_setzen(env,args):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    value = do(env,args[1])
    env[var_name] = value
    return value

def do_abrufen(env,args):
    assert len(args) == 1
    assert isinstance(args[0],str)
    assert args[0] in env, f"Unknown var {args[0]}"
    return env[args[0]]

def do_addieren(env,args):
    assert len(args) == 2
    left = do(env,args[0])
    right = do(env,args[1])
    return left + right

def do_absolutwert(env,args):
    assert len(args) == 1
    value = do(env,args[0])
    return abs(value)

def do_subtrahieren(env,args):
    assert len(args) == 2
    left = do(env,args[0])
    right = do(env,args[1])
    return left - right

def do_abfolge(env,args):
    assert len(args) > 0
    for operation in args:
        result = do(env,operation)
    return result


OPERATIONS = {
    func_name.replace("do_",""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(env,expr):
    if isinstance(expr,int):
        return expr
   
    assert isinstance(expr,list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"
    func = OPERATIONS[expr[0]]
    return func(env, expr[1:])


def main():
    assert len(sys.argv) == 2, "Usage: vars-demo.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program,list)
    env = {}
    result = do(env,program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()