#include"misc.h"
using namespace std;

/* concatenate csv files, asserting headers match and incl. csv header only
once in output at top of file */

int main(int argc, char ** argv){
  str ofn(argv[argc - 1]);
  cout << "data output file: " << ofn << endl;

  size_t i, j;
  if(argc < 3){
    err("usage: csv_cat.cpp [input file] .. [input file n] [output destination]");
  }
  vector<string> filenames;
  for(int j = 1; j < argc - 1; j++){
    str fni(argv[j]);
    filenames.push_back(fni);
  }

  int bad_header = false;
  string header0;
  for(i = 0; i < filenames.size(); i++){
    string header;

    /* check the files open, before we go ahead */
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
      str msg("failed to open input data file: ");
      msg += str(filenames[i]);
      err(msg.c_str());
    }
    dfile.close();
  }
  if(bad_header) return -1;

  ofstream outfile(ofn);
  if(!outfile.is_open()){
    err("failed to write-open file:");
  }
  str line; // line buffer
  time_t t0;
  time(&t0); // start time
  long unsigned int l_i = 0; // row index of output

  string d;
  for(j = 0; j < filenames.size(); j++){
    cout << "data input file: " << filenames[j] << endl;
    ifstream dfile(filenames[j]);

    // read header, discard any header that's not the first
    getline(dfile, line);
    if(l_i ++ == 0){
      outfile << line << endl;
    }
    while(getline(dfile, line)){
      outfile << line << endl;
      l_i ++;
    }
    dfile.close();
  }
  outfile.close();
  return 0;
}
