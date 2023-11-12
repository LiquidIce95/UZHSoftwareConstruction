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




**How to use this framework**

### 3. Tracing

This feature can be used by adding the "--trace file_name" extension to the python command in the CLI.

<code>python lgl_interpreter.py --trace trace_file.log</code>
#### 3.1 Code implementation of logging

In the main function we check if the "--trace" flag is used. If it is used it sets the boolean `tracing = True` and `file` to the file name provided by the command. In an if-statement we check if the `tracing` variable is set to `True` then we add a decorator `log_function` to any function that starts with "do_".

**log_function decorator**

In the log file we want to get the following information about the process: ID, name, start/stop and time. There should be two entries for each do-function that is called. One for when the function was called first (start) and one for when the function was finished (stop). This is the function:

```python3
def log_function(func):
    ID = get_ID()  # 1
    def _inner(envs, args):
        log.append(f"{ID}, {func.__name__}, start, {time_stamp()}") # 2
        res = func(envs, args) # 3
        log.append(f"{ID}, {func.__name__}, stop, {time_stamp()}") # 4
        return res
    return _inner
```

1. We get a unique ID from the `get_ID()` function. This function guarantees that there is no equal six-digit ID's.
2. In the list `log` we save the start time stamp right before we run a "do_" function.
3. We save the output of a "do_" function to `res`. That variable will be returned in the end.
4. In the list `log` we save the stop time stamp right after the "do_" function has been called and its results saved.

**Saving the trace data**

In the main function, after the running of the interpreter, we use the `push()` function to save all entries from the log list in the specified file from the `python3` command.

#### 3.2 Code implementation of reporting

In the `reporting.py` file I have specified the code that is needed to display the report from a log file in the CLI. With the following command you can get the tabular report form printed into the CLI.

`python reporting.py trace_file.log`

In the main function we check if the arguments given from the command are sufficient. If yes, we get the data from the specified log-file and run the `format_report` function.

**format_report(rep: str)**

This function transforms the raw data form the log file into a tabular form for the CLI.
````python3
def format_report(rep: str):
    # remove first line
    k = rep.split("\n") # 1
    r = [el.split(", ") for el in k[1:]] # 2
    d = {}
    for el in r: # 3
        if el[1] not in d.keys():
            d[el[1]] = [1, int(el[3][-6:])]
        elif el[1] in d.keys() and el[2] == "start":
            d[el[1]][0] += 1
            d[el[1]][1] += int(el[3][-6:])
    out = []
    for k, v in d.items(): # 4
        out.append(str_format(k, int(v[0]), int(v[1]), int(int(v[1])/int(v[0]))))
    p = "\n".join(out)
    title_line = f"| Function Name{space(20, len('Function Name'))} | Num. of calls  | Total Time (ms) | Average Time (ms) |"
    spacer = "|-----------------------------------------------------------------------------|"
    return f"{title_line}\n{spacer}\n{p}" # 5
````

1. We part the string by each line.
2. We remove the first line. (Since thats the title)
3. We loop over every line in the list and save the necessary data into the dictionary `d`. If there are two entries (that are not start and stop) we add their duration time.
4. We create the output string for each dictionary key-value pair. This string is formatted by the `str_format` function. That automatically calculates the amount of spaces needed for the table to be fitting.
5. The return value is the correctly formatted table.

The main function prints this output to the CLI.