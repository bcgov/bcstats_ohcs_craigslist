from misc import *
if len(args) < 3: err("usage: select_null [input file] [field name]")

lines = open(args[1]).readlines()
lines = [x.strip().split(',') for x in lines]
hdr = lines[0]
hdr = [x.strip() for x in hdr]
if not args[2] in hdr: err("field name: " + args[2] + " not found in " + str(hdr))
f_i = {hdr[i]: i for i in range(0, len(hdr))}
fii = f_i[args[2]]

print(",".join(hdr))
lines = lines[1:]
for i in range(0, len(lines)):
    w = lines[i]
    w = [x.strip() for x in w]
    if len(w) != len(hdr):
        print("expected len: " + len(hdr))
        print("len(w): " + len(w))
        err("unexpected number of cols, i=" + str(i))
    if w[fii] == '': print(','.join(w))
