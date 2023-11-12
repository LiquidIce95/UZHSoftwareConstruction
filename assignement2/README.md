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