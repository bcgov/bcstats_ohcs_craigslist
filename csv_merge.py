''' convert csv (N files) from columnar format: output 1 csv with N cols

# example of merging two cols together into a new file with two cols:
python3 ../csv_merge.py craigslist-apa-data-bc.csv_id craigslist-apa-data-bc.csv_price
'''
from misc import *

if len(args) < 2:
    print("Error: usage:\n\t python3 csv_merge.py [input 1-col csv filename 1]" + 
          "... [input 1-col csv filename N])")
    sys.exit(1)

# assert we can find all the input files 
files = args[1:]
for i in files:
    if not os.path.exists(i):
        err('could not find input file: ' + str(i))


# check that field name / csv header for 1-col csv, matches extension
fields = {i: i.split('.csv_')[1] for i in files}
i0 = files[0].split('.csv_')[0]
for i in files:
    if i.split('.csv_')[0] != i0:
        err('unexpected')

# open output file
ofn = i0 + '_merged.csv'
f = open(ofn, 'wb')

# new csv header
hdr = [fields[i] for i in files]

# read data from all input files
dat = {}
for i in range(0, len(files)):
    print('+r', files[i])
    dat[i] = open(files[i]).read().split('\n') # doesn't do same thing as readlines()

nrow = len(dat[i])  # print(nrow)
for i in range(0, len(files)):
    nrow_i = len(dat[i])
    # print(nrow_i)
    if nrow_i != nrow:
        err('unexpected nrow')


f.write((','.join(hdr)).encode())
for j in range(1, nrow):
    row = [dat[i][j] for i in range(0, len(files))]
    f.write(('\n' + ','.join(row)).encode())
f.close()
