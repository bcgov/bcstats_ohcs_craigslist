# check expected data files are present:
#   report instances of files that are:
#       * not present
#       * not of expected size
import os
import sys

file_names = ['craigslist-apa-data-bc-html-mar.csv', 'craigslist-bc-apartment-data-mar.csv', 'craigslist-bc-sublets-data-mar.csv', 'craigslist-sublet-data-bc-html-mar.csv', 'craigslist-apa-data-bc.csv', 'craigslist-sublet-data-bc.csv', 'craigslist-apa-data-bc-html-othermeta.csv', 'craigslist-sublet-data-bc-html-othermeta.csv', 'craigslist-apa-data-bc-html-jan.csv', 'craigslist-apa-data-bc-html-sep.csv', 'craigslist-bc-apa-data-jan.csv', 'craigslist-sublet-data-bc-html-jan.csv', 'craigslist-bc-sublet-data-sep.csv', 'craigslist-bc-sublet-data-jan.csv', 'craigslist-bc-apa-data-sep.csv', 'craigslist-sublet-data-bc-html-sep.csv', 'craigslist-bc-apartment-data-apr.csv', 'craigslist-bc-sublets-data-apr.csv', 'craigslist-sublet-data-bc-html-apr.csv', 'craigslist-apa-data-bc-html-apr.csv', 'craigslist-bc-apartment-data-may.csv', 'craigslist-bc-sublets-data-may.csv', 'craigslist-bc-apartment-html-may.csv', 'craigslist-bc-sublets-html-may.csv']

file_sizes = [1313723416, 14167108, 540821, 337123080, 301100188, 15806712, 22868906488, 1207390218, 3277267614, 1913701273, 35371689, 115374402, 727855, 1196955, 21663494, 65148136, 6931814, 218584, 308603553, 648129837, 8114544, 179446, 763264057, 17573827]

hdr = False

for i in range(0, len(file_names)):
    f, fs, f_s = file_names[i], str(file_sizes[i]), None
    f_s = str(os.stat(f).st_size if os.path.exists(f) else 'N/A')
    if fs != f_s:
        if not hdr:
            print("file,bytes expected,bytes")
            hdr = True
        print(','.join([f, fs, f_s]))

if not hdr:
    print("(GOOD) All files present and of expected size")
