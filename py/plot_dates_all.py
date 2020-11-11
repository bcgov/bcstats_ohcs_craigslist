import os
import sys

def run(c):
    print("command: " + c)
    if os.system(c) != 0:
        print("Error: command failed: " + c)
        sys.exit(1)

files = os.popen('ls -1 *join.csv')

for f in files:
    f = f.strip()
    print(f)
    if not os.path.exists(f + '.png'):
        run('python3 plot_dates_file.py ' + f)


