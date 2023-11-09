import sys
import json

def do_addieren(args):
    assert len(args) == 2
    left = do(args[0])
    right = do(args[1])
    return left + right

def do_absolutwert(args):
    assert len(args) == 1
    value = do(args[0])
    return abs(value)

def do_subtrahieren(args):
    assert len(args) == 2
    left = do(args[0])
    right = do(args[1])
    return left - right

def do(expr):
    if isinstance(expr,int):
        return expr

    if expr[0] == "addieren":
        return do_addieren(expr[1:])
    if expr[0] == "absolutwert":
        return do_absolutwert(expr[1:])
    if expr[0] == "subtrahieren":
        return do_subtrahieren(expr[1:])
    
    assert False, f"Unknown operation {expr[0]}"

def main():
    assert len(sys.argv) == 2, "Usage: expr-demo.py filename.gsc"
    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program,list)
    result = do(program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()