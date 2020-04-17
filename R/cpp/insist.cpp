/* assert analog */
#include<Rcpp.h>
#include"misc.h"
using namespace std;
using namespace Rcpp;

//[[Rcpp::export]]
void insist(bool value){
  if(!value){
    err("assertion failed");
  }
}