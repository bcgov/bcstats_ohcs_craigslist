from misc import *
# from ansicolor import *
from bs4 import BeautifulSoup # comment out import, to find upstream dependencies

def parse(args_s): # parse(args_s) where args_s is a string of form html_file,n_records where n_records is the number of records from the "meta" file
    '''parse html data in parallel, to extract relevant segments
    - this is an "initial" coarse parsing, to reduce the volume of "data" by
    removing javascript codes, and other "nondata" portions of the html files
    
    input html files reside in html/
    output results will be put in parsed/
    
    # reminder: make sure to save all intermediary and output files, in a separate
    folder before proceeding to next data set!
    
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
    a = os.system("mkdir -p parsed") # make parsed/ folder if not yet exist
    
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
        if n % 111 == 0: print("\t" + ofn)  # periodic status update
        return ofn
    
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
    parfor(parse_file, inputs)
