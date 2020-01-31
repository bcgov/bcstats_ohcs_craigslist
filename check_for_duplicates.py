'''check for duplicate entries in files in html folder'''
import os
import sys
import time
nrow = int(os.popen('ls -1 html/ | wc -l').read().strip().split()[0])
n, nd = 0, 0
t0, ci = time.time(), 0
for root, dirs, files in os.walk("html", topdown=False):
    for name in files:

        # count number of DOCTYPE html flags, this file:
        fn = os.path.join(root, name)
        d = open(fn).read()
        ns = len(d.split("<!DOCTYPE html>"))
        # print(n)

        n += 1
        if ns > 2:
            nd += 1

        ci += 1
        if ci % 1111 == 0:
            nt = time.time()
            trow = (nt - t0) / (ci + 1)
            trem = trow * (nrow - ci)
            print(fn, ci, ci / nrow, "t", nt - t0, "eta", trem, "eta(h)", trem / 3600.)

print("total", n)
print("duplicates", nd)
print("gross", n + nd)
