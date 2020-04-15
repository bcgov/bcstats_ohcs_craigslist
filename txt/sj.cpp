#include<iostream>
#include<fstream>
#include<stdlib.h>
#include<vector>

using namespace std;

int main(int argc, char ** argv){
  if(argc < 4){
    printf("Error: usage\n\tsj [csv file 1] [csv file 2] .. [csv file n] [output file] # simple join left to right\n");
    exit(1);
  }

  int ninf = argc - 2;
  vector<string> ifn;
  for(int i = 0; i < ninf; i++){
    ifn.push_back(string(argv[i + 1]));
  }

  vector<ifstream> ifile(ninf);
  for(int i = 0; i < ninf; i++){
    ifile[i].open(ifn[i]);
    if(!ifile[i].is_open()){
      printf("Error: failed to open input file: %s\n", ifn[i].c_str());
      exit(1);
    }
  }

  ofstream outf(argv[argc -1]);
  if(!outf.is_open()){
    printf("Error: failed to open output file: %s\n", argv[argc -1]);
    exit(1);
  }

  int i;
  string comma(",");
  vector<string> line(ninf);
  while(std::getline(ifile[0], line[0])){
    for(i = 1; i < ninf; i++){
      if(!std::getline(ifile[i], line[i])){
        printf("Error: failed to read line from other file\n");
        exit(1);
      }
    }

	//    printf("%s\n", line[0].c_str());
    outf << line[0] << comma;

    for(i = 1; i < ninf; i++){
      outf << line[i];
    }
    outf << std::endl;
  }
  outf.close();

  for(int i = 0; i < ninf; i++) ifile[i].close();
  return 0;
}
