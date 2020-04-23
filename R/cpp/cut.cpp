// cut.cpp: this is a C program for debugging binary read file access from byte loc in size_t
//
/* rm a.out; gcc cut.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv 36 50
<!DOCTYPE html>

clear; rm a.out; gcc cut.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv 54284196 54306186*/
#include"misc.h"

int main(int argc, char ** argv){
  if(argc < 4){
    printf("cut.c [filename] [start pos] [end pos] # cut binary file at positions\n");
    exit(1);
  }

  const char * fn = argv[1];
  size_t start_p, end_p;
  sscanf(argv[2], "%zu", &start_p); // no overflow detect
  sscanf(argv[3], "%zu", &end_p);

  // printf("file_name %s start_p %zu end_p %zu\n", fn, start_p, end_p);

  size_t i;
  FILE * f = fopen(fn, "rb");
  if(!f){
    printf("Err: failed to open file: %s\n", fn);
    exit(1);
  }

  char c;
  fseek(f, start_p, SEEK_SET);
  for(size_t i = 0; i <= end_p - start_p; i++){
    c = fgetc(f);
    printf("%c", c);
  }
  return 0;
}