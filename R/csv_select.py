# like csv_select.cpp except resilient to certain kinds of nesting
import os; exists = os.path.exists
import sys; args = sys.argv
import csv
csv.register_dialect('my',
                     delimiter=",",
                     quoting=csv.QUOTE_ALL,
                     skipinitialspace=True)

def err(m): print("Error: " + m); sys.exit(1)
if len(args) < 4: err("usage: python3 csv_select [select file 1 col csv] [select field] [file to select from]")
if not exists(args[1]): err("failed to open select file")
if not exists(args[3]): err("failed to open file to select from")
sf = args[2]

def hdr_lines(f):
    hdr, lines, ci = None, [], 0
    reader = csv.reader(open(f), dialect='my')
    for row in reader:
        if ci == 0: hdr = row
        else: lines.append([y.strip() for y in row])
        ci += 1
    return [hdr, lines]

hdr, lines = hdr_lines(args[1])
if hdr != [sf]: err("expected ['" + sf + "']")
idx = set([x[0] for x in lines])
# print(idx)

hdr, lines = hdr_lines(args[3])
f_i = {hdr[i]: i for i in range(0, len(hdr))}
if not sf in f_i: err("failed to file select field: " + args[3])
sfi = f_i[sf]

ci = 0
for i in range(0, len(lines)):
    if lines[i][sfi] in idx:
        if ci == 0: print(hdr)
        print(lines[i])
        ci += 1