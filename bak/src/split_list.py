# split an index file into subfiles, for distribution e.g.:
#     python3 craigslist-apa-data-bc-html-othermeta.csv_tag
# this file is not used to produce the final product
import os
import sys
import multiprocessing
args = sys.argv
n = multiprocessing.cpu_count()

fn = args[1]
if not os.path.exists(fn):
    print("Error: file not found:", fn)
    sys.exit(1)

lines = open(fn).readlines()
files = [open(fn + "_" + str(i), "wb") for i in range(0, n)]
n_lines = [0  * i for i in range(0, n)]

for i in range(0, len(lines)):
    file_i = i % n
    if n_lines[file_i] > 0:
        files[file_i].write("\n".encode())
    files[file_i].write(lines[i].strip().encode())
    n_lines[file_i] += 1

for i in range(0, n):
    files[i].close()

