import os
import sys
exec(open("py" + os.path.sep + "misc.py").read())
from bs4 import BeautifulSoup # comment out import, to find upstream dependencies

def fp(pattern, soup):
    s = ""
    try:
        s = str(soup.select(pattern)[0])
        s = " ".join(s.strip().split())
    except:
        pass
    s = s.replace('\n', '')
    return s

def parse_file(fn):
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

    patterns = ['.postingtitletext', 
                '.price', 
                '.attrgroup',
                '.mapbox',
                '#postingbody',
                '.notices',
                '.postinginfos']

    ret = [fp(x, soup) for x in patterns]
    ofn = "parsed" + os.path.sep + fn.split(os.path.sep)[-1]
    open(ofn, "wb").write(("\n".join(ret)).encode())
    
    # periodic status update
    n = int(fn.split(os.path.sep)[-1])
    if n % 111 == 0: print("\t" + ofn)
    return ofn  # return output file name

def parse_html(args_s): # parse(args_s) where args_s is a string of form html_file,n_records where n_records is the number of records from the "meta" file
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
    t0, ci, inputs = time.time(), 0, []
    
    # walk the file structure and list the files to parse
    for root, dirs, files in os.walk("html", topdown=False):
        for name in files:
            fn = os.path.join(root, name)  # html filename
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
    parfor(parse_file, inputs)  # need C/C++ version of this
