# convert csv into columnar format: output 1 csv per column
from misc import *

if len(args) < 2:
    err('usage:\n\t python3 csv_split.py [input csv filename]')

in_f, files = args[1], []  # input, outputs

with open(in_f, encoding="utf8", errors='ignore') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    fields, n_fields, rng, ci, is_hdr = None, 0, 0, 0, True

    # for each row of csv
    for row in csvreader:
        row = [r.strip() for r in row]

        if is_hdr:
            # record field names
            fields, n_fields, rng = row, len(row), range(0, len(row))
            filenames, is_hdr = [in_f + '_' + f for f in fields], False

            # open a file per column
            for i in rng:
                print(row[i], filenames[i]) # print({row[i]: filenames[i] for i in rng})
            files = [open(filenames[i], 'wb') for i in rng]
            [files[i].write(fields[i].encode()) for i in rng]

        else:
            # write data row
            if len(row) != len(files):
                print("row", [row])
            print("ci", ci)
            [files[i].write(('\n' + row[i].rstrip()).encode()) for i in rng]
        ci += 1

    [files[i].close() for i in rng]  # close files
    print(ci, "rows written")
