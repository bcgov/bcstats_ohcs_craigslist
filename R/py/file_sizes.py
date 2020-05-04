file_names = ['craigslist-bc-sublets-data-mar.csv', 'craigslist-sublet-data-bc-html-mar.csv', 'craigslist-apa-data-bc.csv', 'craigslist-sublet-data-bc.csv', 'craigslist-apa-data-bc-html-othermeta.csv', 'craigslist-sublet-data-bc-html-othermeta.csv', 'craigslist-apa-data-bc-html-jan.csv', 'craigslist-apa-data-bc-html-sep.csv', 'craigslist-bc-apa-data-jan.csv', 'craigslist-sublet-data-bc-html-jan.csv', 'craigslist-bc-sublet-data-sep.csv', 'craigslist-bc-sublet-data-jan.csv', 'craigslist-bc-apa-data-sep.csv', 'craigslist-sublet-data-bc-html-sep.csv', 'craigslist-bc-apartment-data-apr.csv', 'craigslist-bc-sublets-data-apr.csv', 'craigslist-sublet-data-bc-html-apr.csv', 'craigslist-apa-data-bc-html-apr.csv']
file_sizes = ['540821', '337123080', '301100188', '15806712', '22868906488', '1207390218', '3277267614', '1913701273', '35371689', '115374402', '727855', '1196955', '21663494', '65148136', '6931814', '218584', '308603553', '648129837']

import os
import sys

if len(file_names) != len(file_sizes):
    print("Data entry error: array lengths don't match")
    sys.exit(1)

lines = os.popen("ls -latr *.csv").readlines()
file_names_update, file_sizes_update = [], []

for line in lines:
    line = line.strip()
    line = [x.strip() for x in line.split()]
    sz, fn = line[4], line[8]

    if fn in file_names:
        idx = file_names.index(fn)
        if sz != file_sizes[idx]:
            print("Error: file size mismatch:", fn, "size", sz, "expected", file_sizes[idx])
            sys.exit(1)
    else:
        if fn != "merge.csv" and len(fn.split("join")) < 2:
            print(fn, sz)
            file_names_update.append(fn)
            file_sizes_update.append(sz)

if len(file_names_update) > 0:
    print("file_names_update", file_names_update)
    print("file_sizes_update", file_sizes_update)  
