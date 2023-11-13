

with open("requirements.md","r") as f:
    text = f.read()
    print(text)

f = open("requirements.md","r")
text = f.read()
print(text)
f.close()


# a context manager works this way:
# with CM() as thing:
#    ... do operation ...
#    ... do operation ...