# compare simple with vaderSentiment approach

# need a filter for MOST HAPPY / MOST ANGRY # need a filter for HIGHEST ENTROPY!!!!! # need to describe the stats of each parameter: in terms of distribution

import os; exists = os.path.exists
import sys; args, exit = sys.argv, sys.exit
import numpy as np
import string
import pickle
from copy import deepcopy as cp
def err(m): print('Error: ' + str(m)); exit(1)

files = args[1:]
for f in files:
    if not exists(f):
        err('please check input file:' + str(f))

def remove_punctuation(s):  #return s = "string. With. Punctuation?" # Sample string 
    return s.translate(str.maketrans('', '', string.punctuation)) # for s in w]

# dictionary-based sentiment
valence, lines = {}, open("AFINN-111.txt").readlines()
for line in lines:
    w = line.strip().split()
    w = [''.join(w[:-1]), float(w[-1])]
    w[0] = remove_punctuation(w[0]).lower()
    valence[w[0]] = w[1] # print(w)

def valence_scores(s):
    r = {'neg': 0., 'neu': 0., 'pos': 0., 'compound': 0., 'n/a': 0}
    n1, n2, w = 0., 0, s.split()
    for x in w:
        if x in valence:
            y = valence[x]
            n1 += 1
            if y == 0: r['neu'] += 1. 
            elif y > 0.: r['pos'] += y
            elif y < 0.: r['neg'] -= y
            else: err('impossible')
        else:
            r['n/a'] += 1.
            n2 += 1.
    if n1 > 0.:
        r['neg'] /= n1
        r['pos'] /= n1
        r['neu'] /= n1
    if n1 + n2 > 0:
        r['n/a'] /= (n1 + n2)
    r['compound'] = r['pos'] - r['neg'] # not quite what vader did
    return r

# vader sentiment # python3 -m pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
a = SentimentIntensityAnalyzer()

file_lines = []
for f in files:
    records, term = pickle.load(open(f, 'rb')), 'full_text'
    if not term in records[0]: term = 'text'
    if not term in records[0]: err(str(records[0].keys()))
    file_lines.append(os.popen('python3 print_pkl.py ' + f + ' ' + term).readlines())

for i in range(0, len(file_lines)):
    file_lines[i] = [x.strip('"').strip('"').strip() for x in file_lines[i]] # remove quotes
    file_lines[i] = set(file_lines[i])  # remove redundant records

# sparse vector arithmetic
def s_smul(a, x): return {k: a * x[k] for k in x} # scalar mult left
def s_sdiv(x, a): return {k: x[k] / a for k in x} # scalar div right
def s_mul(x, y): return {k: x[k] * y[k] for k in set(x.keys).intersection(set(y.keys()))} # multiply

def s_add(x, y):
    z = cp(x)
    for k in y: z[k] = z[k] + y[k] if k in z else y[k]
    return z

def s_min(x, y):
    z = cp(x)
    for k in y: z[k] = min(z[k], y[k]) if k in z else y[k]
    return z

def s_max(x, y):
    z = cp(x)
    for k in y: z[k] = max(z[k], y[k]) if k in z else y[k]
    return z

def s_print(x, n=0): # tree print
    if isinstance(x, dict):
        for k in x.keys():
            print(('  ' * n) + "'" + str(k) + "':")
            s_print(x[k], n + 1)
    else:
        print(('  ' * n) + "'" + str(x) + "'")

# calculate sentiment scores
def ms(lines):
    ret = {}
    vs = {'vader': [], 'simpl': []}
    for line in lines:
        line = remove_punctuation(line)
        vs['simpl'].append(valence_scores(line))    # simple sentiment score
        vs['vader'].append(a.polarity_scores(line)) # vader sentiment score
        print('"' + line + '"', '\n\tsimpl', vs['simpl'][-1], '\n\tvader', vs['vader'][-1])

    for k in vs:
        s = vs[k]
        n = len(s)
        vs0 = s[0]
        mn, mx, av = cp(vs0), cp(vs0), cp(vs0)
        for i in range(1, len(s)):
            si = s[i]
            mn = s_min(mn, si)
            mx = s_max(mx, si)
            av = s_add(av, si)
        av = s_sdiv(av, n)
        r = {'min':mn, 'max':mx, 'avg': av}
        ret[k] = r
    return ret

ans = {files[i]: ms(file_lines[i]) for i in range(0, len(file_lines))}
print("ans", ans)
print("---")
s_print(ans)
print("---")

for i in range(0, len(file_lines)):
    f = files[i]
    print(f) # print('\t', ans[f])
    try:
        dates = os.popen('python3 print_pkl.py ' + f + ' date').readlines()
        dates = [x.split()[0].strip() for x in dates]
        dates.sort()
        print("\t", dates[0], dates[-1])
    except:
        print("No date info")
