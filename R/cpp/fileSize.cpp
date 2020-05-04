#include<Rcpp.h>
#include"misc.h"
#include<stdio.h>
#include<stdlib.h>
using namespace std;
using namespace Rcpp;

//[[Rcpp::export]]
R_xlen_t fileSize(StringVector args){
  R_xlen_t n = 0;
  string fn(args[0]);
  return file_size(fn.c_str());
}
