# 20200409 automate the extraction process for a rec'd data blob
import os; exists = os.path.exists
import sys; args = sys.argv
def err(m): print('Error:' + str(m)); sys.exit(1)

def run(c):
    print(c); a = os.system(c);
    if a != 0: err('command failed')
    return a

if len(args) < 3: err('usage: run_extract.py [metadata file (smaller)] [html data file (larger)]')
meta_f, data_f = args[1], args[2]
if not exists(meta_f): err('check file: ' + str(meta_f))
if not exists(data_f): err('check file: ' + str(data_f))

path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep # path to me
print(path)

def rmdir(c):
    if type(c) == list:
        for x in c: rmdir(x)
    else:
        if exists(c) and os.path.isdir(c):
            run('rm -rf ' + c)

rmdir(['html', 'otherAttributes'])
extract = path + 'extract'
if exists(extract): run('rm -f  aextract')
run('rm -f *.csv_tag')

find_start = path + 'find_start'; find_start_c = find_start + '.c'
run('gcc -O4 ' + find_start_c + ' -o ' + find_start)
extract = path + 'extract'; extract_c = extract + '.c'
run('gcc -O4 ' + extract_c + ' -o ' + extract)

run(find_start + ' ' + data_f)
run(extract + ' ' + data_f)
run('python3 ' + path + 'parse.py ' + data_f + ' ' + meta_f)
run('python3 ' + path + 'join.py '  + data_f + ' ' + meta_f)