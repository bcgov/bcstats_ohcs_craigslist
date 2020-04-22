import os
import time
exec(open("py" + os.path.sep + "misc.py").read())
exec(open("py" + os.path.sep + "html_cleanup.py").read())

def join(args_s):
    '''join together the following sources, join on ID number
            1) metadata entry
            2) attr from parsed/ files
            3) attr from otherAttributes/ files '''
    
    args = args_s.split(",")
    if len(args) != 2:
        err('usage: join(html_file,meta_file)')

    in_f , meta_f = args[0], args[1]
    n_skip = 0 # record the number of metadata records, skipped
    
    meta_fields = ['id', 'title', 'url', 'postDate', 'categoryId', 'cityId',
                   'location', 'phoneNumbers', 'contactName', 'emails',
                   'hyperlinks', 'price', 'parsedAddress', 'mapAddress', 'mapLatLng']
    
    html_fields = ['h_price', 'h_bed', 'h_bath', 'h_title', 'h_map_accuracy',
                   'h_map_address', 'h_map_latitude', 'h_map_longitude',
                   'h_map_zoom', 'h_movein_date', 'h_notices', 'h_postingbody',
                   'h_attrgroup', 'h_mapbox', 'h_housing']
    
    # read the metadata file to count the number of records
    nr = int(os.popen('wc -l ' + meta_f).read().strip().split()[0])
    t0 = time.time()  # start timer
    
    out_fn = meta_f + '_merge.csv' # output data, merged file
    print('+w', out_fn)
    outf = open(out_fn, 'wb')
    
    with open(meta_f, encoding="utf8", errors='ignore') as csvfile:
        csvreader, is_hdr = csv.reader(csvfile, delimiter=','), True
        ci, n_fields, rng = 0, 0, 0
        for row in csvreader:
            row = [r.strip() for r in row]
    
            # replace escape commas
            row = [r.replace('\\,',';') for r in row]
    
            # replace actual commas ?
            row = [r.replace(',', ';') for r in row]
    
            if is_hdr:
                hdr = row
                if str(hdr) != str(meta_fields):
                    err('unexpected fields')
    
                new_hdr = [*meta_fields, *html_fields]  # concatenate
                new_hdr.append('otherAttributes') # add otherAttributes
                # add in other set of fields, too
    
                print(','.join(new_hdr))
                is_hdr = False
    
                # write out header
                new_hdr = ','.join(new_hdr)
                outf.write(new_hdr.encode())
    
            else:
    
                if len(row) != len(','.join(row).split(',')):
                    print(row)
                    print(','.join(row).split(','))
                    err('commas')
    
                # id number
                id_s = row[0]
    
                # open parsed html file
                fn = 'parsed' + os.path.sep + id_s
                if not os.path.exists(fn):
                    print('could not find file: ' + str([fn]))
                    n_skip += 1
                    continue
    
                # print("fn", fn)
                fields, line = cleanup_html(fn)
                if len(line.split(',')) != len(html_fields):
                    print(line)
                    err('bad parse: ' + str(len(line)) + ' ' + str(len(html_fields)))
    
                line = line.split(',')
                new_row = [*row, *line]
    
                # open otherAttributes file
                fn2 = 'otherAttributes' + os.path.sep + id_s
                if not os.path.exists(fn2):
                    print('could not find file: ' + str([fn2]))
                    n_skip += 1
                    continue
    
                other = open(fn2).read().strip().strip('!')
                other = other[2:]
                other = other.replace('"', '')
                other = other.replace(';', '&')
                other = other.replace(',', ';')
    
                new_row.append(other)
                new_row = '\n' + ','.join(new_row)
    
                # write out header
                outf.write(new_row.encode())
            ci += 1
    
            if ci % 111 == 0:
                nt = time.time()
                tr = (nt - t0) / (ci + 1)
                trem = tr * (nr - ci)
                print("%" + str(round(100. * float(ci) / float(nr),2)),
                      "t=" + str(round(nt - t0, 2)) + 's',
                      "eta=" + str(round(trem, 2)) + 's',
                      "eta=" + str(round(trem / 3600., 2)) + 'h',
                      "n=" + str(ci))
    print("number of records", ci)
    print("metadata records skipped", n_skip)
