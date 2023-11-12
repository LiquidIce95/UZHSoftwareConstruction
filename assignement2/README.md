## RTFM
## Task 1 additional functionality

### introduction

Our goal was to achieve these features by respecting design choices made in the core little language interpreter (lgl). This includes that arguments of any operation can be integers or operations themselves.

From now on the reader may assume that a presented operation is capable of taking integers or operations as input, unless stated otherwise.

### basic operations

so `multiplizieren,dividieren,potenzieren` are pretty much identical to the arithmetic operations from core lgl.

here is an example

```
["multiplizieren",2,["addieren",2,2]]

@returns
2*(2*2)=8

```

next in order to implement a classical while loop, we needed logical operations:

`kleinergl,kleiner` also adhere to the same principles and can take as arguments integers or other operations.

**important** : all logical operations in lgl return integers, namely 0 or 1.

This design choice is simply due to the fact that core lgl only supports integers and they are sufficient to implement all features in this way.

example:
```
["kleiner",2,3]

@returns
1
```

`gleich` works in the same way

`und,oder` are a bit special in the sense that they first convert the args into booleans (or what the args return, if they are operations themselves) and then with these booleans the `and`, `or` python operators are performed. finally the result is returned as an integer.

with all these logical operations we are cabable of using while loops properly.

**note**: in python, 0 is converted to false and any other integer is converted to true so if the user wants to store `true` in lgl, a non zero integer should be used, conversly for `false`, 0 should be used

### lists, dictionaries and while loops

across multiple programming languages the while loop is pretty consistent, it has a condition which is evaluated upon each iteration and a body of instructions which is executed on each iteration, as long as the condition is true.

It was very important to us to preserve this consistency by implementing the same architecture as stated above this was the main reason why we implemented the logical expressions.

example of `solange`

```
["setzen", "bedingung", 0],
["solange",["kleiner",["abrufen","bedingung"],10],
    ["abfolge",
        ["setzen","bedingung", ["addieren",["abrufen","bedingung"],1]],
        ["drucken",["abrufen","bedingung"]]
    ]
]

@prints
1 to 10
```

obviously, other logical expressions can be used as the condition

`liste` takes an arbitrary amount of arguments but at least one, which is the name of the list.

```
["liste","zettel",["setzen","dachs",9],["addieren",3,4]],

@returns
[9,7]

```

however, once initiated, the length cannot be adjusted

`schauen` allows the user to lookup an entry of a list at a given index

```
["schauen",["abrufen","zettel"],1]

@returns
7

```
**important** it is not enough to write the name of the list object as first argument. The obect must be returned with `abrufen` just like in the core lgl.

Also the **first index starts at 0**, which is common in computer science.


finally `lsetzen` allows us to set a value at a given index, the index must be within the legth of the list object, otherwise the operation is not performed (the programm stops since assertion will be false)

```
["lsetzen",["abrufen","zettel"],1,22]

@returns
[9,22]

```

for this reason we decided to provide `llaenge` which returns the length of a list object, the argument is also the result of the `abrufen` operation.

```
["llaenge",["abrufen","zettel"]]

@returns
2
```

`Wbuch` works just as `liste` with the only difference being that the arguments are pairs of the form ```["key","value"]```

example
```
["Wbuch","zettel2",[["abrufen","bedingung"],3],[["setzen","foo",3],11]],

@returns
{10:3,3:11}

```

`Wsetzen` works jsut as `lsetzten` where the index is now the key

```
["Wsetzen",["abrufen","zettel2"],["abrufen","bedingung"],44],

@returns
{10:44,3:11}

```

the same for `Wschauen`

```
["Wschauen",["abrufen","zettel2"],10]

@returns
44
```


`Wschauen` relies on the key being in the dictionary for this reason can the user check this with. `istdrin`

it is implemented for any iterable object in python so lists and dicitonaries in particular

example

```
["istdrin",["abrufen","neuesBuch"],5],
@returns
1
["istdrin",["abrufen","zettel"],9]

@returns
1
```

where neuesBuch is the output of `mischen`
wich does exactly the same thing as the | operator in pyhton with two dictionaries

example

```
["Wbuch","buch",[3,3],[5,4],[10,200]],
["mischen","neuesBuch",["abrufen","buch"],["abrufen","zettel2"]],
```

all operations are designed in the same way which makes lgl fast to learn since we relied on repeating patterns and design choices.

At this point we felt that we needed to include some if then statemetns since the user will need to check if indices or keys are in the lists or dicitonaries and then proceed depending on the evaluation.

So we also provide `wennDann` 

```
["wennDann",["gleich",2,2],["drucken",3]]

@returns 
the condition after evaluation if the condition was false otherwise if the condition was true it returns the result of the operation executed

```

which is especially useful in combination with `abfolge`

our last feature in this section is `drucken` which simply prints the result of an operation in the same syntax with => onto the console

example

```
["drucken",["abrufen","zettel"]]
```

it works with everything that is also printable in python.

the author notes that it was very tempting to introduce further features but out team decided that this provides a good set of operations which work well in combination with each other.



