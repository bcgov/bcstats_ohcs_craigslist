# generate counts of data observations in a csv
import os
import sys
import time
import operator
from misc import *

if len(sys.argv) < 2:
    err("usage: count.py [csv input file]")

f = open(sys.argv[1])
f_count = open(sys.argv[1] + "_count.csv", "wb")
f_freq = open(sys.argv[1] + "_frequ.csv", "wb")
fields = f.readline().strip().split(",")
print("fields", fields)
ci, occ = 1, [{} for i in range(0, len(fields))]
f_size = os.stat(sys.argv[1]).st_size
ttt = tt = t_0 = time.time()

while True:
    line = f.readline()
    if not line: break
    word = line.strip().split(",")
    if len(word) != len(fields):
        print("warning: incorrect number of fields, line: ", ci)
    for i in range(0, len(word)):
        d = word[i].strip()
        occ[i][d] = 1. if d not in occ[i] else occ[i][d] + 1.
    ci += 1
    if ci % 100000 == 0:
        ttt = tt
        tt = time.time()
        print("file", " %: ", 100. * (float(f.tell()) / float(f_size)), " MB/s:", (float(f.tell()) / 1000000.) / (tt- t_0))#

counts, frequs = [], []
for i in range(0, len(fields)):
    print("sorting field ", fields[i], "..")
    if True:
        n = 0  # number of observations
        occ_i = sorted(occ[i].items(), key=operator.itemgetter(0))
        for j in occ_i:
            n += j[1]
            counts.append(str(fields[i]) + "," + str(j[0]) + "," + str(j[1]))
        occ_i = sorted(occ[i].items(), key=operator.itemgetter(1), reverse=True)
        for k in range(0, len(occ_i)):
            j = occ_i[k]
            j = list(j)
            j[1] = j[1] * (1. / float(n))
            j = tuple(j)
            frequs.append(str(fields[i]) + "," + str(j[0]) + "," + str(j[1]))

# write count table
f_count.write("variable,value,count".encode())
for c in counts:
    f_count.write(('\n' + str(c)).encode())

# write frequency table
f_freq.write("variable,value,frequency".encode())
for f in frequs:
    f_freq.write(('\n' + str(f)).encode())
f_count.close()
f_freq.close()
