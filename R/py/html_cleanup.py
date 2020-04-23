''' finer-grained parsing and clean up, of html files produced by
      extract.cpp
      parse.py

    examples:
        incl. price:    python3 html_cleanup.py parsed/5447094859
        without price:  python3 html_cleanup.py parsed/4760673195'''

import os
sep = os.path.sep
from bs4 import BeautifulSoup
exec(open("py" + sep + "misc.py").read())
exec(open("py" + sep + "strtok.py").read())  # reticulate-friendly import?

def fp(soup, pattern): # use beautifulsoup to parse out a pattern from the doc
    s = ""
    try:
        s = str(soup.select(pattern)[0])
        s = " ".join(s.strip().split())
    except Exception:
        pass
    return s.replace('\n', '')

def cleanse(s):
    return s.replace(',', '').replace('\n', '').replace('\r', '').strip()

def html_cleanup(fn):
    data = {}
    if not os.path.exists(fn):
        err("Error: could not find file: " + str(fn))

    html = open(fn).read()  # open the data
    soup = BeautifulSoup(html, 'lxml')  # parse the data

    # results from fp() get keyed w./ tag, minus symbol prefix \in {., #}
    tags = ['.price',
            '.housing',
            '#titletextonly',
            '.attrgroup',
            '#postingbody',
            '.notices',
            '.mapbox']

    for s in tags:
        data[s[1: ]] = fp(soup, s)

    data['postingbody'] = data['postingbody'].replace('<br/>','')
    data['postingbody'] = data['postingbody'].replace('<section id="postingbody">','')
    data['postingbody'] = data['postingbody'].replace('</section>','')
    data['postingbody'] = " ".join(data['postingbody'].split())
    data['notices'] = data['notices'].replace('<ul class="notices">', '')
    data['notices'] = data['notices'].replace('<li>', '')
    data['notices'] = data['notices'].replace('</ul>', '')
    data['notices'] = data['notices'].replace('</li>', '')

    # clean up price:
    try:
        # strip outer tags, remove $ sign
        p = data['price']
        p = strtok(p, '>')[1]
        p = strtok(p, '<')[0]
        p = p.strip('$')
        data['price'] = p
    except Exception: pass

    # clean up housing
    try:
        # strip outer tags and remove $ sign
        h = data['housing']
        h = strtok(h, '>')[1]
        h = strtok(h, '<')[0]
        data['housing'] = h
    except Exception: pass

    # clean up housing
    data['title'] = ''
    try:
        # strip outer tags and remove $ sign
        t = data['titletextonly']
        t = strtok(t, '>')[1]
        t = strtok(t, '<')[0]
        del data['titletextonly']
        data['title'] = t
    except Exception: pass

    # clean up attrgroup e.g.: ['<p class="attrgroup"><span><b>3</b>BR / <b>1.5</b>Ba</span> <span><b>1150</b>ft<sup>2</sup></span>']
    a = data['attrgroup'].strip()
    data['attrgroup'] = a

    # get number of bedrooms
    bed = ''
    try:
        bed = a.split('<b>')[1].split('</b>')[0]
    except Exception: pass
    data['bed'] = bed

    # clean up bed
    b = bed.lower()
    if len(b) > 2:
        if b[-2:] == 'br':
            bed = bed[:-2]
            data['bed'] = bed

    # get number of bathrooms
    bath = ''
    try:
        x = a.split('<b>')[2].split('</b>')[0]
        bath = x
    except Exception: pass
    data['bath'] = bath

    # remediate empty bath variable
    if bath == '':
        try:
            if len(a.split('Ba<')) < 2:
                pass
            elif len(a.split('>Ba')) < 2:
                # negative: e.g. parsed/4841847119
                # positive: e.g. parsed/6134742515
                x = a.split('Ba<')[0]
                x = x.split('<b>')[1]
                bath = x.strip()
        except Exception: pass
    data['bath'] = bath

    # clean up bath
    b = bath.lower()
    if len(b) > 2:
        if b[-2:] == 'ba':
            bath = bath[:-2]
            data['bath'] = bath

    movein_date = '' # get move_in date
    try:
        x = a.split(' date=')
        if len(x) > 2:
            logf = open('logfile.txt', 'ab')
            logf.write(('\nerror,movein_date,id,' + fn).encode())
            #err('movein_date: date= error')
            logf.close()
        x = x[1]
        x = x.split('" ')[0]
        x = x.strip('"')
        data['movein_date'] = x
    except Exception:
        data['movein_date'] = ''

    # clean up postingbody
    b = data['postingbody']
    try:
        b = b.split('<a class="showcontact"')[0].strip()
    except Exception: pass
    data['postingbody'] = b.replace('&amp;','&')

    # clean up mapbox
    m = data['mapbox']
    accuracy, latitude, longitude, address, mapzoom = '', '', '', '', ''

    # clean up data accuracy
    try:
        accuracy = m.split('data-accuracy="')[1]
        accuracy = accuracy.split('"')[0]
    except Exception: pass
    data['map_accuracy'] = accuracy

    # clean up latitude
    try:
        latitude = m.split('data-latitude="')[1]
        latitude = latitude.split('"')[0]
    except Exception: pass
    data['map_latitude'] = latitude

    # clean up longitude
    try:
        longitude = m.split('data-longitude="')[1]
        longitude = longitude.split('"')[0]
    except Exception: pass
    data['map_longitude'] = longitude

    # clean up address
    try:
        address = m.split('<p class="mapaddress">')[1]
        address = address.split('<small>')[0]
    except Exception: pass
    data['map_address'] = address


    # clean up map url
    try:
        mapzoom = m.split('<a href="')[1].split(',')[2].split('"')[0]
    except Exception: pass
    data['map_zoom'] = mapzoom.strip('z')


    # cleanse strings of unfriendly characters (for csv)
    for d in data:
        data[d] = cleanse(data[d])

    if False:
        for d in data:
            print(d, "\n", [data[d]], "\n")

    # pragmatic programming: explicitly order the elements

    elems = ['price', 'bed', 'bath', 'title', 'map_accuracy', 'map_address', 'map_latitude', 'map_longitude', 'map_zoom', 'movein_date', 'notices', 'postingbody', 'attrgroup', 'mapbox', 'housing']

    dat = [data[d] for d in elems]
    dat = ','.join(dat)
    if len(dat.split(',')) != len(elems): err('encoding error')
    fields = ','.join(['h_' + e for e in elems])
    return fields, dat

    # notes: e.g.: parsed/6663814110 failed to parse movein_date
