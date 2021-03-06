#include"misc.h"
// rm extract; gcc -O4 extract.c -o extract; ./extract craigslist-apa-data-bc-html-othermeta.csv
// note: should delete the html and otherAttributes folders before (re)running
//
// the program can use append mode for writing files, to catch records with same ID:
//   see line: int duplicates = 0; // to ignore duplicates by taking latest record

/*
 wc -l craigslist-apa-data-bc.csv
1231197 craigslist-apa-data-bc.csv
*/

int go_to(FILE * f, const char * tag, size_t tag_len, char * buf, size_t * next, size_t * fp){
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

    // read the stuff from the match position to confirm
    fseek(f, *fp, SEEK_SET);
    size_t br = fread(&buf[0], sizeof(char), tag_len, f);
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

char fgetc2(FILE * f){
  fseek(f, -1, SEEK_CUR);
  char c = fgetc(f);
  fseek(f, -1, SEEK_CUR);
  return c;
}

void cr(FILE * f){
  // return to start of a line

  size_t fp = ftell(f); // where are we?
  if(fp == 0) return; // done if at beginning of file

  char c;
  do{
    c = fgetc2(f);
  }
  while(c != '\n');

  while(c == '\n' || c == '\r'){
    c = fgetc(f);
  }
  fseek(f, -1, SEEK_CUR); // back one
}

int main(int argc, char ** argv){
  int duplicates = 0;
  int a = system("mkdir -p html");
  a = system("mkdir -p otherAttributes"); // some random stuff that was stuffed in next to the html, yikes!

  int debug = 0; // apply this to print statments in a moment

  size_t next, fp;
  const char * end_tag = "</html>";
  size_t tag_len = (size_t) strlen(end_tag);
  char * buf = (char *)(void *)malloc(tag_len + 1);
  for(next = 0; next < tag_len + 1; next++){
    buf[next] = '\0';
  }
  next = 0;

  time_t t0; time(&t0);
  clock_t c0 = clock();

  const char * fn = argv[1];
  size_t infile_size = file_size(fn); // file size
  FILE * f = fopen(fn, "rb");

  const char * tf;
  if(argc < 3){
    tf = strcat(argv[1], "_tag");
  }
  else{
    // allow an option to read from separate file, for parallelism case
    tf = argv[2];
  }

  FILE * g = fopen(tf, "rb");
  if(!f) err("failed to open input file"); // the file itself
  if(!g) err("failed to open start tag file *_tag: run find_start.c first"); // html start tag file
  size_t n;
  char ** s = (char **) alloc(sizeof(char *));;
  *s = NULL;

  size_t i = 0;
  do{
    n = gs(g, s);
    if(n < 1) break;

    size_t start_p;
    sscanf(*s, "%zu", &start_p);
    fseek(f, start_p, SEEK_SET);
    n = gs(f, s);

    // now find end tag
    next = 0;
    while(!go_to(f, end_tag, tag_len, buf, &next, &fp));

    // this is the span of the html
    if(debug) printf("\n%zu %zu\n", start_p, fp + tag_len - 1);

    // now just need to apply CR and grab the start tag, and we've split the file
    fseek(f, start_p, SEEK_SET);
    cr(f);
    n = gs(f, s);
    if(debug){
      prints(*s, n);
      printf("\n"); // print start tag
    }

    const char * id_s = strtok(*s, ",");
    size_t id;
    sscanf(*s, "%zu,", &id); // don't need strtok to get the number
    if(debug) printf("[%zu]\n", id);

    const char * pre = "html/";
    char * t = alloc(strlen(pre) + strlen(id_s) + 1);
    strcpy(t, pre);
    strcpy(t + strlen(pre), id_s);
    t[strlen(pre) + strlen(id_s)] = '\0';

    // output file name
    FILE * h = fopen(t, duplicates?"ab":"wb");

    // secondary file to save otherAttributes string
    const char * pre2 = "otherAttributes/";
    char * t2 = alloc(strlen(pre2) + strlen(id_s) + 1);
    strcpy(t2, pre2);
    strcpy(t2 + strlen(pre2), id_s);
    t2[strlen(pre2) + strlen(id_s)] = '\0';
    if(debug){
      printf("\n%s\n", t2);
    }
    FILE * j = fopen(t2, duplicates?"ab":"wb");

    // write html to file, here:
    size_t dat_sz = fp + tag_len - start_p;
    char * dat = alloc(dat_sz);

    // copy from file to memory
    fseek(f, start_p, SEEK_SET);
    size_t nr = fread(dat, sizeof(char), dat_sz, f);
    size_t nw = fwrite(dat, sizeof(char), dat_sz, h);

    if(nr != nw) err("write fail");
    fclose(h);
    free(dat);

    if(debug){
      printf("%s\n", t);
    }
    free(*s);
    *s = NULL;

    // zoom over any newline, to get to next record
    char c = fgetc(f);
    while(c == '\n' || c == '\r') c = fgetc(f);
    fseek(f, -1, SEEK_CUR); // go back


    // sometimes the otherdata field is blank, need a new counter
    size_t n2 = gs(f, s);
    if(debug){
      prints(*s, n2);
      printf("\n");
    }
    size_t nw2 = fwrite(*s, sizeof(char), strlen(*s), j);
    fclose(j);

    if(++i % 1000 == 0){
      float frac = 100. * (float)fp / (float)infile_size;
      // time_t t1;  time(&t1);
      float dt = (float)(clock() - c0) / (float) CLOCKS_PER_SEC; // (float)t1 - (float)t0;
      float nps = (float)fp / dt;
      float eta = (float)(infile_size - fp) / nps;
      printf("%%%.3f +w %s eta: %fs i=%zu\n", frac, t, eta, i );
    }
    free(t);
  }
  while(n > 0);

  // end program
  free(*s);

  time_t t1;
  time(&t1);
  printf("dt %fs\n", (float)(t1 - t0));

  return 0;
}
