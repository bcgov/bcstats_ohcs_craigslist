import os; exists = os.path.exists
import sys; args = sys.argv

def err(m):
    print("Error:", m); sys.exit(1)

def run(c):
    print(c)
    if os.system(c) != 0:
        err("command failed: " + c)

f = args[1]

if not exists(f):
    err("could not find input csv file: " + f)

if not exists('tmp'):
    os.mkdir('tmp')

if not exists('cpp/csv_split.exe'):
    run('g++ -O4 cpp/csv_split.cpp cpp/misc.cpp -o cpp/csv_split.exe')
    if not exists('cpp/csv_split.exe'):
        err("need to compile cpp/csv_split.cpp")

run(' '.join(['cp', f, 'tmp']))
run('cpp/csv_split.exe tmp/' + f)
run('python3 plot_dates.py ' + 'tmp/' + f + '_postDate' + ' ' + f)
