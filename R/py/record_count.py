from misc import *
lines = open("data_file_sizes.txt").readlines()
lines = [x.strip().strip(',') for x in lines]
hdr, lines = lines[0].split(','), lines[1:]
f_i = {hdr[i]: i for i in range(0, len(hdr))}

out = ["meta_file", "meta_file_nbytes",
       "html_file", "html_file_nbytes",
       "meta_file_n_rows",
       "html_file_n_html_tags",
       "html_file_avg_bytes_per_html_tag",
       "proj_html_file_size_from_ratio_and_meta_files_n_rows"]
print(','.join(out))

for i in range(0, len(lines)):
    x = lines[i].split(',')
    mfi = f_i['meta_file']
    hfi = f_i['html_file']
    mfsi= f_i['meta_file_size']
    hfsi= f_i['html_file_size']
    mf, hf, mfs, hfs = x[mfi], x[hfi], int(x[mfsi]), int(x[hfsi])

    tf = hf + '_tag'
    if not exists(tf):
        err('no tag file: ' + tf)

    tn = int(os.popen('wc -l ' + tf).read().strip().split()[0])
    mn = int(os.popen('wc -l ' + mf).read().strip().split()[0]) - 1 # less one for header
    out = [mf, mfs, hf, hfs, mn, tn, round(hfs / tn, 1), round((hfs / tn) * mn, 1)]
    out = [str(x) for x in out]
    print(','.join(out))

