# library("reticulate")
# py_install("bs4")
# py_install("html5lib")
# py_install("lxml")

import os
import sys
import csv
import time
args = sys.argv

def err(msg):
    print("Error: " + str(msg))
    sys.exit(1)

def parfor(my_function, my_inputs):
    # evaluate function in parallel, and collect the results
    if os.name != 'nt':
        import multiprocessing as mp
        pool = mp.Pool(mp.cpu_count())
        result = pool.map(my_function, my_inputs)
        return(result)
    else: # no can do in Windows! Ha ha
        ret = []
        for i in my_inputs:
            ret.append(my_function(i))
        return(ret)
