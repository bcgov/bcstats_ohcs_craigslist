import os
import sys
from misc import * 
from bs4 import BeautifulSoup # comment out import, to find upstream dependencies

def fp(soup, pattern):
    s = ""
    try:
        s = str(soup.select(pattern)[0])
        s = " ".join(s.strip().split())
    except:
        pass
    s = s.replace('\n', '')
    return s

def parse_file(fn):
    html = open(fn, "rb").read().decode().strip()
    html = html.replace('""', '"')
    soup = BeautifulSoup(html, 'lxml')
    # print("title", soup.title.string)

    # discard info not inside html tag
    if 'html' not in soup.contents:
        # print("soup.contents", soup.contents)
        # err("expected html in soup.contents")
        # on windows, everything is inside the html tag.
        pass
    else:
        for c in soup.contents:
            if c.name == 'html':
                soup = c
                break
    patterns = ['.postingtitletext',
                '.price',
                '.attrgroup',
                '.mapbox',
                '#postingbody',
                '.notices',
                '.postinginfos']

    ret = [fp(soup, x) for x in patterns]

    ofn = "parsed" + os.path.sep + fn.split(os.path.sep)[-1]
    open(ofn, "wb").write(("\n".join(ret)).encode())

    # periodic status update
    n = int(fn.split(os.path.sep)[-1])
    if n % 222 == 0:
        print("\t" + ofn)
    return ofn  # return output file name

def html_parse(args_s): # parse(args_s) where args_s is a string of form html_file,n_records where n_records is the number of records from the "meta" file
    print("html_parse", str(args_s))
    # if __name__ != "__main__":
    #     return
    '''
    input html files reside in html/
    output results will be put in parsed/

    tested linux vm:
      python3 -m pip install bs4
      python3 -m pip install lxml
      python3 -m pip install  bs4 --upgrade
      python3 split.py'''

    args = args_s.split(",")
    if len(args) != 2:
        err("bad parameters: commas in filenames are bad")

    in_f = args[0] # unused this script, file where html/ came from e.g., craigslist-apa-data-bc-html-sep.csv
    nrow = int(args[1]) # row count from metadata file

    if not os.path.exists("parsed"):
        os.mkdir("parsed") # make "parsed" folder
    t0 = time.time()
    ci = 0
    inputs = []

    # walk the file structure and list the files to parse
    for root, dirs, files in os.walk("html" + os.path.sep, topdown=False):
        for name in files:
            fn = os.path.join(root, name)  # html filename
            number = 0
            is_number = False
            try:
                number = int(name)
                is_number = True
            except:
                err("is_number test: failed on name='" + str(name) + "'")

            if is_number:  # skip a phantom file that exists in windows for some reason?
                inputs.append(fn)  # add it to the list to process "in parallel" (not on windows)

            # simple progress bar
            ci += 1
            if ci % 222 == 0:
                nt = time.time()
                trow = (nt - t0) / (ci + 1)
                trem = trow * (nrow - ci)
                print(ci, ci / nrow, "t", nt - t0, "eta", trem, "eta(h)", trem / 3600.)
    
    for i in range(0, len(inputs)):
        if not os.path.exists(inputs[i]):
            print("Error: file not found: " + str(inputs[i]))
    
    # execute in parallel
    parfor(parse_file, inputs)  # need C/C++ version of this?
