'''parse html data in parallel, to extract relevant segments
- this is an "initial" coarse parsing, to reduce the volume of "data" by
removing javascript codes, and other "nondata" portions of the html files

input html files reside in html/
output results will be put in parsed/

instructions to run:
    python3 parse.py apa # for apartments dataset
    python3 parse.py sublet # for sublet dataset

# reminder: make sure to save all intermediary and output files, in a separate
folder before proceeding to the other data set

tested linux vm:
  python3 -m pip install bs4
  python3 -m pip install lxml
  python3 -m pip install  bs4 --upgrade
  python3 split.py'''

from misc import *
from ansicolor import *
from bs4 import BeautifulSoup # comment out import, to find upstream dependencies

flag, in_f = args[1], None
if flag == 'apa':
    pass
elif flag == 'sublet':
    pass
else:
    err("input flag must be \in {'apa', 'sublet'}")

# unused this script, this is where the data in html/ came from
in_f = 'craigslist-' + flag + '-data-bc-html-othermeta.csv'

# read metadata to get approx records count
meta_f = 'craigslist-' + flag + '-data-bc.csv'

'''
use unix terminal to get row count for status meter:

wc -l craigslist-sublet-data-bc.csv
    67494 craigslist-sublet-data-bc.csv
'''
nrow = int(os.popen('wc -l ' + meta_f).read().strip().split()[0])


# make the directory parsed/
a = os.system("mkdir -p parsed")

def parse(fn):
    html = open(fn).read()
    html = html.replace('""', '"')
    soup = BeautifulSoup(html, 'lxml')
    # print("title", soup.title.string)

    # discard info not inside html tag
    if 'html' not in soup.contents:
        err("expected html in soup.contents")

    for c in soup.contents:
        if c.name == 'html':
            soup = c
            break

    def fp(pattern):
        s = ""
        try:
            s = str(soup.select(pattern)[0])
            s = " ".join(s.strip().split())
        except:
            pass
        s = s.replace('\n', '')
        return s

    ret = []
    ret.append(fp('.postingtitletext'))
    ret.append(fp('.price'))
    ret.append(fp('.attrgroup'))
    ret.append(fp('.mapbox'))
    ret.append(fp('#postingbody'))
    ret.append(fp('.notices'))
    ret.append(fp('.postinginfos'))
    
    ofn = "parsed" + os.path.sep + fn.split(os.path.sep)[-1]
    n = fn.split(os.path.sep)[-1]
    n = int(n)
    open(ofn, "wb").write(("\n".join(ret)).encode())
    if n % 111 == 0:
        print("\t" + ofn)
    return ofn

t0 = time.time()

ci = 0
inputs = []

# walk the file structure and list the files to parse
for root, dirs, files in os.walk("html", topdown=False):
    for name in files:

        # html filename
        fn = os.path.join(root, name)

        inputs.append(fn)  # add it to the list to process in parallel

        # simple progress bar
        ci += 1
        if ci % 111 == 0:
            nt = time.time()
            trow = (nt - t0) / (ci + 1)
            trem = trow * (nrow - ci)
            print(ci, ci / nrow, "t", nt - t0, "eta", trem, "eta(h)", trem / 3600.)

# run the html parsing in parallel
print("start parfor")
parfor(parse, inputs)
