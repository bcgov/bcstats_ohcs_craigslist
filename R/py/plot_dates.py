import os
import datetime
import sys; args = sys.argv

month_only = False # change to true to trunate to first of month

# e.g., input file: out.csv_unique-id-_.csv_postdate
if len(args) < 2:
    print("Error: usage: python3 print_dates.py [input file 1 col csv]")
    sys.exit(1)

source_file = None
if len(args) > 2:
    source_file = args[2]
if not os.path.exists(source_file):
    print("Error: file not found: " + source_file)
    sys.exit(1)


'''
postdate
2014-11-14T05:00:02Z
'''
lines = open(args[1]).readlines()[1:]

print("stripping..")
lines = [line.strip() for line in lines]

print("slicing..")
lines = [line.split('T')[0] for line in lines]

print("convert..")

n_na = 0
dates = []
for i in range(0, len(lines)):
    lines[i] = lines[i].split("T")[0]
    #print(lines[i])
    #print("split", lines[i].split("-"))
    try:
        y, m, d = lines[i].split('-')
        dates.append(datetime.datetime(int(y), int(m), int(d) if not month_only else 1))
    except:
        n_na += 1.

print("number of NA", n_na)

count = {}
print("accumulating..")

for i in range(0, len(dates)):
    d = dates[i]
    if d not in count:
        count[d] = 0.
    count[d] += 1.

counts = []
for c in count:
    counts.append([c, count[c]])
import operator

print("counts", counts)

print("sorting..")
counts.sort(key=operator.itemgetter(0))

x, y = {}, {}
for d in counts:
    dt, c = d
    yy, mm, dd = int(dt.year), int(dt.month), int(dt.day)
    if yy not in x:
        x[yy], y[yy] = [], []
    x[yy].append(datetime.datetime(2020, mm, dd))
    y[yy].append(c)

import matplotlib.pyplot as plt
fig= plt.figure(figsize=(12,5))
for yy in x:
    plt.plot(x[yy],y[yy], label=str(yy))
plt.legend()
plt.title("data counts by month and year")
plt.tight_layout()
plt.savefig((source_file if source_file is not None else args[1]) + '.png')
plt.show()
