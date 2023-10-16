def test(*args : any)->None:
    for arg in args:
        print(f"{arg} some blabla", end = " ")



if __name__ == "__main__":
    test(1,2,3,4)