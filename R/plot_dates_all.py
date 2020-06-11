import os
import sys

def run(c):
    print(c)
    if os.system(c) != 0:
        print("Error: command failed")
        sys.exit(1)

files = os.popen('ls -1 *join.csv')

for f in files:
    f = f.strip()
    print(f)
    run('python3 plot_dates_file.py ' + f)


