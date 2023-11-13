def outer(value):
    def inner(current):
        print(f"Inner sum is {current + value}")
    
    print(f"Outer value is {value}")

    for i in range(3):
        inner(i)

outer(10)