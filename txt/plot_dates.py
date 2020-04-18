import os
import datetime
import sys; args = sys.argv


# e.g., input file: out.csv_unique-id-_.csv_postdate
if len(args) < 2:
    print("Error: usage: python3 print_dates.py [input file 1 col csv]")
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

dates = []
for i in range(0, len(lines)):
    y, m, d = lines[i].split('-')
    dates.append(datetime.datetime(int(y), int(m), 1)) #  int(d))) 

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

print("sorting..")
counts.sort(key=operator.itemgetter(0))


x = {}
y = {}
for d in counts:
    dt, c = d
    yy = int(dt.year)
    mm = int(dt.month)
    dd = int(dt.day)

    if yy not in x:
        x[yy] = []
        y[yy] = []

    x[yy].append(datetime.datetime(2020, mm, dd))
    y[yy].append(c)


import matplotlib.pyplot as plt
for yy in x:
    plt.plot(x[yy],y[yy], label=str(yy))
plt.legend()
plt.title("data counts by month and year")
plt.tight_layout()
plt.show()