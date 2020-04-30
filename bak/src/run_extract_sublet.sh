# clear files
rm -rf html
rm -rf otherAttributes
rm -f extract
rm -f craigslist-sublet-data-bc-html-othermeta.csv_tag

# extract html start tags
gcc -O4 find_start.c -o find_start 
./find_start craigslist-sublet-data-bc-html-othermeta.csv

# extract html tags
gcc -O4 extract.c -o extract
./extract craigslist-sublet-data-bc-html-othermeta.csv

# set permissions
chmod 777 *
