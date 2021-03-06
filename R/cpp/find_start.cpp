/* clear; rm a.out; gcc -O4 find_start.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv */
#include<Rcpp.h>
#include"misc.h"
using namespace std;
using namespace Rcpp;

FILE *f, *g, *h; // linear, random access, and write handles
const char * start_tag = "<!DOCTYPE html>"; // tag to match

int match(const char * tag, size_t tag_len, char * buf, size_t * next, size_t * fp){
  if(*next == 0){
    // if we're at the start of a match, record the present position
    *fp = ftell(f);
  }

  char c = fgetc(f);
  if(c != tag[(*next)++]){
    // failed to match a char
    *next = 0;
    return 0;
  }

  if(*next == tag_len){
    // if we matched the whole tag
    *next = 0;
    fprintf(h, "%zu\n", *fp);

    // read the stuff from match position
    fseek(g, *fp, SEEK_SET);
    size_t br = fread(&buf[0], sizeof(char), tag_len, g);
    if(br != tag_len){
      printf("Err: br != tag_len\n");
      exit(1);
    }
    buf[tag_len] = '\0';

    // printf("match: buf[%s]\n", buf);
    if(strncmp(buf, tag, tag_len) != 0){
      printf("Err: mismatch\n");
      exit(1);
    }
    return 1;
  }
  return 0;
}

//[[Rcpp::export]]
int find_start(StringVector args){
  int argc = args.size();
  if(argc != 1) err("find_start [input csv filename]");
  string arg(args[0]);

  size_t next, fp;
  size_t start_tag_len = (size_t) strlen(start_tag); // set up variables
  // printf("%zu\n", start_tag_len);
  char * buf = (char *)(void *)malloc(start_tag_len + 1);
  for(next = 0; next < start_tag_len + 1; next++){
    buf[next] = '\0';
  }
  next = fp = 0;

  time_t t0; // start clock and open files
  time(&t0);
  f = fopen(arg.c_str(), "rb");
  g = fopen(arg.c_str(), "rb");

  string c(arg + string("_tag"));
  h = fopen(c.c_str(), "wb");
  if(!h){
    str msg("failed to open file:");
    msg += str(c);
    err(msg.c_str());
  }

  fseek(f, 0L, SEEK_END); // get file size
  size_t fs = ftell(f);
  printf("file size (bytes): %zu\n", fs);

  rewind(f);
  rewind(g);

  size_t i;
  size_t n_match = 0;
  for(i = 0; i < fs; i++){
    if(i < fp) continue; // delete this?

    int result = match(start_tag, start_tag_len, buf, &next, &fp);

    if(result == 1){
      n_match += 1;
    }

    if(i % 10000000 == 0){
      printf("%f\n", 100. * ((float)(i + 1) / (float)fs));
    }
  }
  Rprintf("n_match %zu\n", n_match);
  // printf("n %ld\n", (long int)n);
  free(buf);
  fclose(f);
  fclose(g);
  fclose(h);
  return 0;
}