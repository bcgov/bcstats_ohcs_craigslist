// cut.cpp: this is a C program for debugging binary read file access from byte loc in size_t
//
/* rm a.out; gcc cut.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv 36 50
<!DOCTYPE html>

clear; rm a.out; gcc cut.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv 54284196 54306186*/
#include"misc.h"

int main(int argc, char ** argv){
  if(argc < 4){
    err("cut.c [filename] [start pos] [end pos] # cut binary file at byte pos. 0-indexed, inclusive\n");
  }

  size_t e_p, s_p;
  const char * fn = argv[1];
  sscanf(argv[2], "%zu", &s_p); // no overflow detect
  sscanf(argv[3], "%zu", &e_p); // printf("file_name %s start_p %zu end_p %zu\n", fn, s_p, e_p);

  FILE * f = fopen(fn, "rb");
  if(!f) err(str("failed to open file: ") + str(fn));

  fseek(f, s_p, SEEK_SET);
  for(size_t i = s_p; i <= e_p; i++) printf("%c", fgetc(f));

  fclose(f);
  return 0;
}
