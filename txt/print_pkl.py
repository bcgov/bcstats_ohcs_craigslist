# print out object hierarchy from pkl file
import os
import re
import sys
import pickle

if len(sys.argv) < 2:
    print("Error: usage\n\tpython print_pkl [.pkl file name]")
    print("\tpython print_pkl [.pkl file name] [key e.g. full_text]")
    print("\tpython print_pkl [.pkl file name] [key e.g. user] [secondary key e.g. location]")
    sys.exit(1)

key, key2 = None, None
if len(sys.argv) > 2:
    key = sys.argv[2]
    if len(sys.argv) > 3:
        key2 = sys.argv[3]

# https://machinelearningmastery.com/clean-text-machine-learning-python/
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

pkl_file = pickle.load(open(sys.argv[1], 'rb'))
for obj in pkl_file:

    if key2 is not None:
        print(obj[key][key2])
    else:
        if key is not None:
            s = ' '.join(str(obj[key]).strip().split())
            if key == 'full_text' or key == 'text':
                s = remove_url(s)
                s = s.lower()
                import string
                s = s.translate(str.maketrans('', '', string.punctuation))
                s = '"' + s + '"'
            print(s.strip())
        else:
            print(obj.keys())
            for k in obj.keys():
                try:
                  s = str(obj[k].keys())
                  print("\t" +str(k) + ' --> ' + s)
                except:
                  print("\t" +str(k).replace('\n', ' '))
            sys.exit(1)

# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/calculate-tweet-word-frequencies-in-python/
# place 
''' fig, ax = plt.subplots(figsize=(8, 8))

# Plot horizontal bar graph
.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="purple")
ax.set_title("Common Words Found in Objs (no stop or collect words)")
plt.show()'''
