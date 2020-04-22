import os
import sys
import csv
import time
args = sys.argv

def err(msg):
    print("Error:" + str(msg))
    sys.exit(1)

def parfor(my_function, my_inputs):
    # evaluate function in parallel, and collect the results
    import multiprocessing as mp
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(my_function, my_inputs)
    return(result)