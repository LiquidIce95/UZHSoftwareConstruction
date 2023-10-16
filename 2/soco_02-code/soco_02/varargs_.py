def show_args(first,second,*args,**kwargs):
    print(f"first = {first}")
    print(f"second = {second}")
    print(f"args = {args}")
    print(f"kwargs = {kwargs}")


#show_args("alberto")
show_args("alberto","python","course","design",42,course="Software Construction")

print(1,23,4,5,6)