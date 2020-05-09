#!/usr/bin/env bash
test ! -f csv_sort.exe   && g++ -O3 csv_sort.cpp   misc.cpp -o csv_sort.exe
test ! -f csv_slice.exe  && g++ -O3 csv_slice.cpp  misc.cpp -o csv_slice.exe
test ! -f csv_select.exe && g++ -O3 csv_select.cpp misc.cpp -o csv_select.exe
test ! -f csv_unique.exe && g++ -O3 csv_unique.cpp misc.cpp -o csv_unique.exe
test ! -f snip.exe 	 && g++ -O3 snip.cpp       misc.cpp -o snip.exe
