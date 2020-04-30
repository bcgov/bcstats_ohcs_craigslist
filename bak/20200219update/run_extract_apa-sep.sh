# clear files
rm -rf html
rm -rf otherAttributes
rm -f extract
rm -f *.csv_tag
mv -f craigslist-bc-apartment-data-sep.csv craigslist-bc-apa-data-sep.csv

# extract html start tags
gcc -O4 find_start.c -o find_start 
# extract html tags
gcc -O4 extract.c -o extract

# four steps
./find_start     craigslist-apa-data-bc-html-sep.csv
./extract        craigslist-apa-data-bc-html-sep.csv
python3 parse.py craigslist-apa-data-bc-html-sep.csv craigslist-bc-apa-data-sep.csv
python3 join.py  craigslist-apa-data-bc-html-sep.csv craigslist-bc-apa-data-sep.csv

# set permissions
chmod 777 *
