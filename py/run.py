import os
import sys
from join import join as join
from html_parse import html_parse as html_parse

def err(m):
    print('Error: ' + m); sys.exit(1)

def run(m):
    print(m)
    a = os.system(m)
    if a != 0: err("command failed: " + m)

# assert system is Mac or Linux
try:
    import posix
except:
    ImportError: err('Mac OS and Linux supported')

def run_cpp(cpp_file, args, collect_output = False):
    print("run_cpp", cpp_file, args)
    ext = cpp_file[-4:]
    if(ext != '.cpp'):
        err('filename must end in .cpp')

    fn = cpp_file[0: -4]
    exe, sep = fn + '.exe', os.path.sep
    file_path = sep.join(__file__.split(sep)[0: -1]) + sep + 'cpp' + sep
    
    # might not need initial separator
    if file_path[0:5] != '/home': 
        file_path = file_path.lstrip(sep)

    if not os.path.exists(file_path + exe):
        cmd = 'g++ -O4 ' + (file_path + cpp_file) + ' ' + file_path + "/misc.cpp" + ' -o ' + (file_path + exe)
        print(cmd)
        a = os.system(cmd)

    cmd = file_path + './' + exe + ' ' + ' '.join(args)
    if collect_output:
        output = os.popen(file_path + './' + exe + ' ' + ' '.join(args)).read()
        print(output)
        return output
    else:
        print(cmd)
        a = os.system(cmd)
        return a

def chunks(s, chunk_len):
    s = s.replace('.', '-')
    x = s.split('-')
    for i in range(0, len(x)):
        ci = x[i]
        x[i] = ci[0: min(chunk_len, len(ci))]
    return x

def mkdir(p):
    if not os.path.exists(p):
        os.mkdir(p)


def harmari_craigslist_parsing(html_file, meta_file):
    print('harmari_craigslist_parsing', html_file, meta_file)

    join_file = meta_file + '_join.csv'

    if os.path.exists(join_file):
        print('file extracted:', join_file)
        return

    print('  1. start index..')
    if not os.path.exists(html_file + '_tag'):
        run_cpp('find_start.cpp', [html_file])

    print('  2. start extract..')
    mkdir('html')
    mkdir('otherAttributes')
    run_cpp('extract.cpp', [html_file])

    print('  3. count records..')
    n_records = run_cpp('lc.cpp', [meta_file], True).strip()

    print('  4. parse html..')
    to_parse = html_parse(','.join([html_file, n_records]))

    print('  5. join html and metadata..')
    join([html_file, meta_file, n_records])
    print('done')


def match_infiles(in_dir = './'):
    join_files = []
    html, meta, outp = [], [], []
    
    files = os.popen('ls -1 ' + in_dir + '*.csv').read().strip().split('\n')
    files = [x.strip().strip('.').strip('/') for x in files]

    for f in files:
        hdr = run_cpp('head.cpp', [f], True)
        if hdr == "id,html,otherAttributes":
            html.append(f)
        elif hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng":
            meta.append(f)
        elif hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng,h_price,h_bed,h_bath,h_title,h_map_accuracy,h_map_address,h_map_latitude,h_map_longitude,h_map_zoom,h_movein_date,h_notices,h_postingbody,h_attrgroup,h_mapbox,h_housing,otherAttributes":
            outp.append(f)
        else:
            err("unrecognized file: " + f)

    print("html", html)
    print("meta", meta)
    print("outp", outp)
    html_match, meta_match = [], []

    for i in range(0, len(html)):
        s = html[i]
        x = chunks(s, 3)
        n_x, max_j, max_s = len(x), 0, 0
    
        for j in range(0, len(meta)):
            score = 0
            mj = meta[j]
            x1 = x[0]
            y = chunks(mj, 3)
            n_y = len(y)

            for k in range(0, len(y)):
                if y[k] in x:
                    score += 1
        
            score = 2. * score / (n_x + n_y)
        
            if score > max_s: max_j, max_s = j, score
            print("**score", score, "html:", html[i], "meta:", meta[j])
        
        print("  ->score:", max_s, "html:", html[i], "meta:", meta[max_j])
        html_match.append(html[i])
        meta_match.append(meta[max_j])

    for i in range(0, len(html_match)):
        html_file, meta_file = html_match[i], meta_match[i]
        run("rm -rf ./html/")
        run("rm -rf ./otherAttributes/")
        run("rm -rf ./parsed/")
        join_file = meta_file + "_join.csv"
        harmari_craigslist_parsing(html_file, meta_file)
        join_files.append(join_file)

    # print("6. concatenate csv files together")
    join_files.append("csv_cat.csv")
    run_cpp('csv_cat.cpp',join_files)

match_infiles()
