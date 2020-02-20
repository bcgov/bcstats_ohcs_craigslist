/* clear; rm a.out; gcc -O4 find_start.c; ./a.out craigslist-apa-data-bc-html-othermeta.csv */
#include"misc.h"

FILE *f, *g, *h; // linear, random access, and write handles
const char * start_tag = "<!DOCTYPE html>"; // tag to match

int match(const char * tag, size_t tag_len, char * buf, size_t * next, size_t * fp){
  if(*next == 0){
    // if we're at the start of a match, record the present position
    *fp = ftell(f);
  }

  char c = fgetc(f);
  if(c != tag[(*next)++]){
    // if we failed to match a char
    *next = 0;
    return 0;
  }
  else{
    // we matched a char
    // printf("%c,next=%zu\n", c, *next);
  }

  if(*next == tag_len){
    // if we matched the whole tag
    *next = 0;
    fprintf(h, "%zu\n", *fp);

    // read the stuff from the match position
    fseek(g, *fp, SEEK_SET);
    size_t br = fread(&buf[0], sizeof(char), tag_len, g);
    if(br != tag_len){
      printf("Err: br != tag_len\n");
      exit(1);
    }
    buf[tag_len] = '\0';
    // printf("buf[%s]\n", buf); // print out match
    if(strncmp(buf, tag, tag_len) != 0){
      printf("Err: mismatch\n");
      exit(1);
    }

    return 1;
  }
  return 0;
}

int main(int argc, char ** argv){
  size_t next, fp;
  size_t start_tag_len = (size_t) strlen(start_tag); // set up variables
	//  printf("%zu\n", start_tag_len);
  char * buf = (char *)(void *)malloc(start_tag_len + 1);
  for(next = 0; next < start_tag_len + 1; next++){
	  buf[next] = '\0';
  }
  next = fp = 0;

  time_t t0; // start clock and open files
  time(&t0);
  f = fopen(argv[1], "rb");
  g = fopen(argv[1], "rb");
  h = fopen(strcat(argv[1], "_tag"), "wb");

  fseek(f, 0L, SEEK_END); // get file size
  size_t fs = ftell(f);
  rewind(f);
  rewind(g);

  size_t i;
  for(i = 0; i < fs; i++){	  
    if( i < fp) continue;  // delete this?

    match(start_tag, start_tag_len, buf, &next, &fp);
    if(i % 100000000 == 0){
      printf("%f\n", 100. * ((float)(i + 1) / (float)fs));
    }
  }

 //  printf("n %ld\n", (long int)n);
  free(buf);
  fclose(f);
  fclose(g);
  fclose(h);
  return 0;
}
