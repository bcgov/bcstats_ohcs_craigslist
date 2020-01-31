import os
import sys
import csv
args = sys.argv
in_f, fields, files = args[1], [], []

with open(in_f, encoding="utf8", errors='ignore') as csvfile:
    csvreader, is_hdr = csv.reader(csvfile, delimiter=','), True
    ci, n_fields, rng = 0, 0, 0
    for row in csvreader:
        ci += 1
print("number of records", ci)
