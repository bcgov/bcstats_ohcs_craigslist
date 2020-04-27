# convert a csv format file, to a pkl file that print_pkl.py and sentiment.py expect
# should probably just rewrite the sentiment program to not need this translation, instead
import os
import sys
import pickle

if len(sys.argv) < 2:
    print("Error: usage:\n\tpython3 csv2pkl [csv input file]")
    sys.exit(1)

inf, of = open(sys.argv[1], 'rb'), open(sys.argv[1] + '.pkl', 'wb')
hdr = inf.readline().decode().strip().split(',')
dump, ix = [], range(0, len(hdr))

ci = 0
while True:
    line = inf.readline()
    if line is None: break

    w = line.decode().strip()
    if w == '': continue

    w = w.split(',')
    if len(w) != len(hdr):
        print(len(w), w)
        print("Error: len(w) != len(hdr): ci=" + str(ci))
        sys.exit(1)
    
    # write json object to file 
    dump.append({hdr[i]: w[i] for i in ix})
    ci += 1

print("dumping..")
pickle.dump(dump, of)
