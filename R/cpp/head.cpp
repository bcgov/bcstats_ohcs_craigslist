#include<Rcpp.h>
#include"misc.h"
#include<stdio.h>
#include<stdlib.h>
using namespace std;
using namespace Rcpp;

//[[Rcpp::export]]
str head(StringVector args){
  if(args.size() != 1) err("head.cpp: [filename]");

  str fn(args[0]);
  FILE * f = fopen(fn.c_str(), "rb");

  char * s = NULL;
  char ** sp = &s;

  gs(f, sp);
  str ret(s);

  // printf("%s\n", s);
  free(s);
  return ret;
}