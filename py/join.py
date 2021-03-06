import os
import time
from misc import *
from html_cleanup import *

def assert_remove(fn):
    if not os.path.exists(fn):
        err("file did not exist: " + str(fn))

    os.remove(fn)

    if os.path.exists(fn):
        err("file not removed: " + str(fn))
    # print("rm " + str(fn))

def join(args):
    print(args)
    '''join together the following sources, join on I D number
            1) metadata entry -- if available :D
            2) attr from parsed/ files
            3) attr from otherAttributes/ files'''

    # args = args_s.split(",")
    if len(args) != 3:
        err('usage: join(html_file,meta_file,line_count_meta_file)')
    in_f , meta_f, nr, n_skip = args[0], args[1], int(args[2]), 0

    meta_fields = ['id', 'title', 'url', 'postDate', 'categoryId', 'cityId',
                   'location', 'phoneNumbers', 'contactName', 'emails',
                   'hyperlinks', 'price', 'parsedAddress', 'mapAddress', 'mapLatLng']

    html_fields = ['h_price', 'h_bed', 'h_bath', 'h_title', 'h_map_accuracy',
                   'h_map_address', 'h_map_latitude', 'h_map_longitude',
                   'h_map_zoom', 'h_movein_date', 'h_notices', 'h_postingbody',
                   'h_attrgroup', 'h_mapbox', 'h_housing']

    t0 = time.time()  # start timer
    out_fn = meta_f + '_join.csv' # output data, merged file
    print('+w', out_fn)
    outf = open(out_fn, 'wb')

    ld = os.listdir('html')
    open(".listdir_1.txt", "wb").write(("\n".join(ld)).encode())


    # for each meta record
    with open(meta_f, encoding="utf8", errors='ignore') as csvfile:
        csvreader, is_hdr = csv.reader(csvfile, delimiter=','), True
        ci, n_fields, rng = 0, 0, 0

        for row in csvreader:
            row = [r.strip() for r in row]
            row = [r.replace('\\,',';') for r in row]  # repl. escape commas
            row = [r.replace(',', ';') for r in row]  # repl. actual commas?

            if is_hdr:
                # now reading the header of the meta file
                hdr = row
                if str(hdr) != str(meta_fields):
                    print("hdr", hdr)
                    print("meta_fields", meta_fields)
                    err('unexpected fields')

                new_hdr = [*meta_fields, *html_fields]  # concatenate
                new_hdr.append('otherAttributes') # add otherAttributes
                print(','.join(new_hdr))  # add in other set of fields too
                new_hdr, is_hdr = ','.join(new_hdr), False
                outf.write(new_hdr.encode())  # write out header

            else:
                # now reading a record of the meta file
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

                fields, line = html_cleanup(fn)

                ret = line.split(",")
                # -----------------------------------------------------------------
                if len(ret) != len(html_fields):
                    print(line)
                    err('bad parse: ' + str(len(line)) + ' ' + str(len(html_fields)))

                for i in range(0, len(ret)):
                    x = ret[i]

                    if len(x) < 1:
                        continue

                    if x[0] == "<" and x[-1] == ">":
                        # assume a simple set of outer tags to remove
            
                        li, ri = -1, len(x) # right close of left outer tag, left close of right outer tag

                        for j in range(1, len(x)):
                            if x[j] == ">":
                                li = j
                                break
            
                        for j in range(len(x) - 1, 0, -1):
                            if x[j] == "<":
                                ri = j
                                break

                        # can remove tags
                        if li >= 0 and ri < len(x) and li < ri:
                            ret[i] = x[li + 1: ri]  # so, remove them
                        ret[i] = ret[i].strip("$")
                # ----------------------------------------------------------------
                line = ",".join(ret)

                assert_remove('html' + os.path.sep + id_s)
                assert_remove(fn)  # delete file so we know which html records aren't in meta_file

                line = line.split(',')
                new_row = [*row, *line]

                # open otherAttributes file
                fn2 = 'otherAttributes' + os.path.sep + id_s
                if not os.path.exists(fn2):
                    print('could not find file: ' + str([fn2]))
                    n_skip += 1
                    continue

                other = open(fn2, 'rb').read()
                try:
                    other = other.decode('latin-1')
                except Exception:
                    other = other.decode('utf-8')

                assert_remove(fn2) # delete file so we know which otherAttrs records not in meta_file

                other = other.strip().strip("!")
                other = other[2:]
                other = other.replace('"', '')
                other = other.replace(';', '&')
                other = other.replace(',', ';')

                new_row.append(other)
                new_row = '\n' + ','.join(new_row)
                outf.write(new_row.encode())  # write out header

            if ci % 111 == 0:
                nt = time.time()
                tr = (nt - t0) / (ci + 1)
                trem = tr * (nr - ci)
                pct_s = str(round(100. * float(ci) / float(nr),2)).zfill(4)
                if pct_s[0] == '0':
                    pct_s = ' ' + pct_s[1:]
                print("%" + pct_s,
                      "t=" + str(round(nt - t0, 2)) + 's',
                      "eta=" + str(round(trem, 2)) + 's',
                      "eta=" + str(round(trem / 3600., 2)) + 'h',
                      "n=" + str(ci))
            ci += 1

    print("number of records, meta only", ci)
    ld = os.listdir('html')
    open(".listdir_2.txt", "wb").write(("\n".join(ld)).encode())

    for id_s in ld:
        new_row = ['' for i in range(0, len(meta_fields))]
        new_row[0] = id_s

        # should probably mod out the common code sections here!
        id_s = id_s.strip()
        # open parsed html file
        fn = 'parsed' + os.path.sep + id_s
        if not os.path.exists(fn):
            print('could not find file: ' + str([fn]))
            n_skip += 1
            continue

        # print("fn", fn)
        fields, line = html_cleanup(fn)
        if len(line.split(',')) != len(html_fields):
            print(line)
            err('bad parse: ' + str(len(line)) + ' ' + str(len(html_fields)))

        assert_remove('html' + os.path.sep + id_s)
        assert_remove(fn)  # delete file so we know which html records aren't in meta_file

        line = line.split(',')
        new_row = [*new_row, *line]

        # open otherAttributes file
        fn2 = 'otherAttributes' + os.path.sep + id_s
        if not os.path.exists(fn2):
            print('could not find file: ' + str([fn2]))
            n_skip += 1
            continue

        other = open(fn2, 'rb').read()
        try:
            other = other.decode('latin-1')
        except Exception:
            other = other.decode('utf-8')

        assert_remove(fn2) # delete file so we know which otherAttrs records not in meta_file

        other = other.strip().strip("!")
        other = other[2:]
        other = other.replace('"', '')
        other = other.replace(';', '&')
        other = other.replace(',', ';')

        new_row.append(other)
        new_row = '\n' + ','.join(new_row)
        outf.write(new_row.encode())  # write out header
        ci += 1

    print("number of records, total", ci)
    print("metadata records skipped", n_skip)
