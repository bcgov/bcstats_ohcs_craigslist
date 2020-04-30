# perform simple summary stats: min, max, mean, stdv
# on a columnar dataset, e.g. produced by csv_split.cpp
# 
# for exclusion of bad data, lower and upper bounds on input,
# are specified at terminal
from misc import *

if len(args) < 4:
    print('stats.py: simple stats on column data\n' +
        '- min, max and mean calculated\n' +
        '- lower and upper bounds for the above, are specified as parameters,\n' + 
        '  in interest of excluding bad data')
    err('usage:\n  stats.py [input 1-col file] [lower] [upper]')

f, min_thres, max_thres = open(args[1]), float(args[2]), float(args[3])

# min, max, average, count, excluded, ignored, lines
mn, mx, av, nx, n_out, n_nn, n, x = 0, 0, 0, 0, 0, 0, 0, []

# for each line in the file:
while True:
    line = f.readline()
    if not line:
        break
    else:
        n += 1  # line count
    d = None
    try:
        d = float(line)
        if d < min_thres or d > max_thres:
            n_out += 1  # value parsed to number but excluded from calc
            continue
        nx += 1  # value included in calc
        x.append(d)
    except Exception:
        n_nn += 1  # value not parsed to number

    # calculation
    if d is not None:
        mn = d if nx == 1 else mn
        mx = d if nx == 1 else mx
        mn = d if d < mn else mn
        mx = d if d > mx else mx
        av += d
av /= nx
print("min", round(mn, 5))
print("max", round(mx, 5))
print("avg", round(av, 5))

import math
dx = 0
for xi in x:
    dd = av - xi
    dx += dd * dd
    
print("stdv", round(math.sqrt(dx / nx), 5))
print("n_calc", nx)
print('---')

print("total lines in file", n)
print("non-numeric values", n_nn)
print("numeric values excluded", n_out)
