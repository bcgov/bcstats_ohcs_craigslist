import os
import sys

def err(m):
    print("Error: " + m)
    sys.exit(1)

lines = open("data_file_sizes.txt").readlines()
lines = [x.strip().strip(",").split(",") for x in lines]
hdr = lines[0]
f_i = {hdr[i]: i for i in range(0, len(hdr))}
lines = lines[1:]

html_file = {x[f_i['meta_file']]: x[f_i['html_file']] for x in lines}

#for k in html_file:
#    print(k, html_file[k])

nf = ["craigslist-apa-data-bc.csv_join.csv_null.csv",
      "craigslist-bc-sublets-data-apr.csv_join.csv_null.csv",
      "craigslist-bc-sublets-data-mar.csv_join.csv_null.csv"]

for f in nf:
    mf = f.split("_join")[0]
    hf = html_file[mf]

    fs = f + "_slice.csv"
    cmd = "./cpp/csv_slice.exe " + f + " id "
    # print(cmd)
    a = os.system(cmd)

    selected_file = mf + "_select.csv"
    cmd = "python3 csv_select.py " + fs + " id " + mf + " > " + selected_file
    a = os.system(cmd)

    if not os.path.exists(selected_file):
        err("failed to produce selected_file")

    if open(selected_file).read().strip() != "":
        err("assertion failed")

    hsf = hf + "_select.csv"
    cmd = "python3 csv_vselect.py " + fs + " id " + hf + " DOCTYPE  > " + hsf
    if not os.path.exists(hsf):
        print("not exists: " + hsf)
        print(cmd)
        a = os.system(cmd)

    print(os.popen("wc -l " + hsf).read())
