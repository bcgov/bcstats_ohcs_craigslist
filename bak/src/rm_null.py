# excise nulls from file
from misc import *

if len(args) < 2:
    err('python3 rm_null.py [input file]')

fn = args[1]
if not os.path.exists(fn):
    err('failed to find input file: ' + fn)

f, ofn = open(fn), fn + '_rmnull'
of = open(ofn, 'wb')

# for each line of input, write out denulled line
while True:
    line = f.readline()
    if not line:
        break
    of.write(line.replace('\0', '').encode())
of.close()
