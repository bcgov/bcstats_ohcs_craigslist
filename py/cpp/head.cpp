#include"misc.h"
#include<stdio.h>
#include<stdlib.h>
using namespace std;

string head(string fn){
  FILE * f = fopen(fn.c_str(), "rb");
  
  char * s = NULL;
  char ** sp = &s;
  
  gs(f, sp);
  str ret(s);

  // printf("%s\n", s);
  free(s);
  return ret;
}

int main(int argc, char ** argv){
  if (argc < 2) err("head.cpp: [filename]");
  cout << head(string(argv[1]));

  return 0;
}

