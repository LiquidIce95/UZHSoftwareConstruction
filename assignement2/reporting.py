import sys

title_line = "| Function Name  | Num. of calls  | Total Time (ms) | Average Time (ms) |"
spacer = "|-----------------------------------------------------------------------|"

def get_report(name: str):
    with open(name, "r") as f:
        report = f.read()
        f.close()
    return report

def space(a, b):
    sp = ""
    for i in range(0, a - b):
        sp += " "
    return sp

def str_format(fname: str, calls: int, tot: int, av: int):
    t = round(tot/1000000, 3)
    a = round(av/1000000, 3)
    # 14, 14, 15, 16
    return f"|   {fname}{space(12, len(fname))} |       {str(calls)}{space(8, len(str(calls)))} |      {str(t)}{space(10, len(str(t)))} |      {str(a)}{space(12, len(str(a)))} |"

def format_report(rep: str):
    # remove first line
    k = rep.split("\n")
    r = [el.split(", ") for el in k[1:]]
    d = {}
    for el in r:
        if el[1] not in d.keys():
            d[el[1]] = [1, int(el[3][-6:])]
        elif el[1] in d.keys() and el[2] == "start":
            d[el[1]][0] += 1
            d[el[1]][1] += int(el[3][-6:])
    out = []
    for k, v in d.items():
        out.append(str_format(k, int(v[0]), int(v[1]), int(int(v[1])/int(v[0]))))
    p = "\n".join(out)
    return f"{title_line}\n{spacer}\n{p}"

def main():
    if len(sys.argv) > 0:
        if sys.argv[1] == "trace_file.log":
            report = get_report("trace_file.log")
            format = format_report(report)
            print(format)
    else:
        raise Warning("Correct usage: python reporting.py <log file name>")

if __name__ == "__main__":
    main()