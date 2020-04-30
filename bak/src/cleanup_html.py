''' fine-grained parsing and clean up of html files produced by
     1) extract.c
     2) parse.py
    
    example incl. price:
     python3 cleanup_html.py parsed/5447094859
    
    example of one without price:
        python3 cleanup_html.py parsed/4760673195
'''
from misc import *
from strtok import strtok
from bs4 import BeautifulSoup
 
data = {}

def cleanup_html(fn):
    global data
    data = {}
    if not os.path.exists(fn):
        err("Error: could not find file: " + str(fn))
    
    html = open(fn).read()  # open the data
    soup = BeautifulSoup(html, 'lxml')  # parse the data
    
    # use beautifulsoup to parse out a pattern from the doc
    def fp(pattern):
        s = ""
        try:
            s = str(soup.select(pattern)[0])
            s = " ".join(s.strip().split())
        except:
            pass
        return s.replace('\n', '')
    
    data = {}
    
    
    # parse out a pattern and enter it into a dict variable
    def rt(s):
        global data
        data[s[1: ]] = fp(s)
    
    # results from fp() get keyed w./ tag, minus symbol prefix \in {., #}
    tags = ['.price',
            '.housing',
            '#titletextonly',
            '.attrgroup',
            '#postingbody',
            '.notices',
            '.mapbox']
    
    [rt(t) for t in tags] # list comprehension syntax instead of for loop
    
    data['postingbody'] = data['postingbody'].replace('<br/>','')
    data['postingbody'] = data['postingbody'].replace('<section id="postingbody">','')
    data['postingbody'] = data['postingbody'].replace('</section>','')
    data['postingbody'] = " ".join(data['postingbody'].split())
    
    data['notices'] = data['notices'].replace('<ul class="notices">', '')
    data['notices'] = data['notices'].replace('<li>', '')
    data['notices'] = data['notices'].replace('</ul>', '')
    data['notices'] = data['notices'].replace('</li>', '')
    
    
    # clean up price
    try:
        # strip outer tags and remove $ sign
        p = data['price']
        p = strtok(p, '>')[1]
        p = strtok(p, '<')[0]
        p = p.strip('$')
        data['price'] = p
    except Exception:
        pass
    
    # clean up housing
    try:
        # strip outer tags and remove $ sign
        h = data['housing']
        h = strtok(h, '>')[1]
        h = strtok(h, '<')[0]
        data['housing'] = h
    except Exception:
        pass
    
    # clean up housing
    data['title'] = ''
    try:
        # strip outer tags and remove $ sign
        t = data['titletextonly']
        t = strtok(t, '>')[1]
        t = strtok(t, '<')[0]
        del data['titletextonly']
        data['title'] = t
    except Exception:
        pass
    
    # clean up attrgroup
    # e.g.: ['<p class="attrgroup"><span><b>3</b>BR / <b>1.5</b>Ba</span> <span><b>1150</b>ft<sup>2</sup></span>']
    a = data['attrgroup'].strip()
    data['attrgroup'] = a
    
    bed = ''  # get no of bedrooms
    try:
        x = a.split('<b>')[1].split('</b>')[0]
        bed = x
    except Exception:
        pass
    data['bed'] = bed

    # clean up bed
    b = bed.lower()
    if len(b) > 2:
        if b[-2:] == 'br':
            bed = bed[:-2]
            data['bed'] = bed



    bath = ''  # get number of bathrooms
    try:
        x = a.split('<b>')[2].split('</b>')[0]
        bath = x
    except Exception:
        pass
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
        except Exception:
            pass
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
    except Exception:
        pass
    data['postingbody'] = b.replace('&amp;','&')
    
    # clean up mapbox
    m = data['mapbox']
    accuracy, latitude, longitude, address, mapzoom = '', '', '', '', ''
    
    try:  # clean up data accuracy
        accuracy = m.split('data-accuracy="')[1]
        accuracy = accuracy.split('"')[0]
    except Exception:
        pass
    data['map_accuracy'] = accuracy
    
    try:  # clean up latitude
        latitude = m.split('data-latitude="')[1]
        latitude = latitude.split('"')[0]
    except Exception:
        pass
    data['map_latitude'] = latitude
    
    try:  # clean up longitude
        longitude = m.split('data-longitude="')[1]
        longitude = longitude.split('"')[0]
    except Exception:
        pass
    data['map_longitude'] = longitude
    
    try:  # clean up address
        address = m.split('<p class="mapaddress">')[1]
        address = address.split('<small>')[0]
    except Exception:
        pass
    data['map_address'] = address
    
    
    try:  # clean up map url
        mapzoom = m.split('<a href="')[1].split(',')[2].split('"')[0]
        # https://www.google.com/maps/search/?api=1&query=
        # https://www.google.com/maps/search/?api=1&query=47.5951518,-122.3316393,10z
    except Exception:
        pass
    data['map_zoom'] = mapzoom.strip('z')
    
    
    def cleanse(s):
        return s.replace(',', '').replace('\n', '').replace('\r', '').strip()
    
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
    
    if len(dat.split(',')) != len(elems):
        err('encoding error')
    
    fields = ','.join(['h_' + e for e in elems])
    return fields, dat

# for test purposes only
if __name__ == '__main__':
    fn = sys.argv[1]
    fields, data = cleanup_html(fn)
    print([fields])
    print([data])

'''
notes: 
    parsed/6663814110 failed to parse movein_date
'''

