#include"misc.h"
#include<vector>
#include<string>
#include<fstream>
#include<iostream>
#define str string
using namespace std;

/* concatenate csv files, asserting headers match and incl. csv header only
once in output at top of file */

int main(int argc, char ** argv){
  int i, j;
  if(argc < 2) err("usage: csv_cat.cpp [input file] .. [input file n]");

  vector<string> filenames;
  for(i = 1; i < argc; i++) filenames.push_back(string(argv[i]));

  int bad_header = false;
  string header0;
  for(i = 0; i < filenames.size(); i++){
    string header;

    /* check all the files actually open before we go ahead */
    std::ifstream dfile(filenames[i]);
    getline(dfile, header);
    if(i == 0){
      header0 = header;
    }
    if(header0 != header){
      cout << "error: file :" << filenames[i] << " header:\n\t" << header << " didn't match first header: \n\t" << header0 << endl;
      bad_header = true;
    }

    if(!dfile.is_open()){
      err("failed to open input data file:");
    }
    dfile.close();
  }
  if(bad_header) return 1;

  str ofn(string("csv_cat.csv"));
  cout << "data output file: " << ofn << endl;
  ofstream outfile(ofn);
  if(!outfile.is_open()) err("failed to write-open file:");

  str line; // line buffer
  time_t t0;
  time(&t0); // start time
  time_t t1;
  long unsigned int l_i = 0; // row index of output
  long unsigned int c_i = 0;

  cout << "writing.." << endl;
  string d;
  for(j = 0; j < filenames.size(); j++){
    cout << "data input file: " << filenames[j] << endl;
    ifstream dfile(filenames[j]);

    // read header, discard any header that's not the first
    getline(dfile, line);
    if(l_i ++ == 0) outfile << line << endl;
    while(getline(dfile, line)){
      outfile << line << endl;
      l_i ++;
    }
    dfile.close();
  }
  outfile.close();
  return 0;
}
