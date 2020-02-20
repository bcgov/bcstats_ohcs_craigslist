# clear files
rm -rf html
rm -rf otherAttributes
rm -f extract
rm -f *.csv_tag

mv -f craigslist-bc-sublets-data-sep.csv craigslist-bc-sublet-data-sep.csv

craigslist-bc-sublet-data-sep.csv
craigslist-sublet-data-bc-html-sep.csv

# extract html start tags
gcc -O4 find_start.c -o find_start 
# extract html tags
gcc -O4 extract.c -o extract

# four steps
./find_start     craigslist-sublet-data-bc-html-sep.csv
./extract        craigslist-sublet-data-bc-html-sep.csv
python3 parse.py craigslist-sublet-data-bc-html-sep.csv craigslist-bc-sublet-data-sep.csv
python3 join.py  craigslist-sublet-data-bc-html-sep.csv craigslist-bc-sublet-data-sep.csv

# set permissions
chmod 777 *
