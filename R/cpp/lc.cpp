#include<Rcpp.h>
#include"misc.h"
#include<stdio.h>
#include<stdlib.h>
using namespace std;
using namespace Rcpp;

//[[Rcpp::export]]
R_xlen_t lc(StringVector args){
  char c = '\0';
  R_xlen_t n = 0;
  string fn(args[0]);

  FILE * fp = fopen(fn.c_str(), "rb");
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
