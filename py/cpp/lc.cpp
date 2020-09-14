#include"misc.h"
#include<stdio.h>
#include<stdlib.h>
using namespace std;

size_t lc(string arg){
  char c = '\0';
  size_t n = 0;

  FILE * fp = fopen(arg.c_str(), "rb");
  if(fp == NULL){
    err("failed to open file");
  }
  do{
    c = fgetc(fp);
    if(c == '\n'){
      n++;
    }
  }
  while(c != EOF);
  fclose(fp);

  return n;
}

int main(int argc, char ** argv){
  if(argc < 2) err("lc.cpp [filename]");

  printf("%zu\n", lc(string(argv[1])));
  return 0;
}

