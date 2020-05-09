# 20200508 like csv_select.cpp except doesn't parse the target into fields: parses into lines only
import os; exists = os.path.exists
import sys; args = sys.argv
import csv
csv.register_dialect('my',
                     delimiter=",",
                     quoting=csv.QUOTE_ALL,
                     skipinitialspace=True)

def err(m): print("Error: " + m); sys.exit(1)
if len(args) < 4: err("usage: python3 csv_vselect [select file 1 col csv] [select field] [file to select from]")
if not exists(args[1]): err("failed to open select file")
if not exists(args[3]): err("failed to open file to select from")
sf = args[2]

corroborant = None
try: corroborant = args[4]
except: pass

def hdr_lines(f):  # only use this for reading the 1-col file
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

lines = open(args[3]).readlines()
hdr = lines[0]
print(hdr.strip(), end="")
if corroborant is None:
    for i in range(0, len(lines)):
        found, line = False, lines[i]
        for j in idx:
            if j in line:
                found = True
        if found: print('\n' + line.strip(), end="")
else:
    for i in range(0, len(lines)):
        found, line = False, lines[i]
        if corroborant in line:
            for j in idx:
                if j in line:
                    found = True
        if found: print('\n' + line.strip(), end="")
