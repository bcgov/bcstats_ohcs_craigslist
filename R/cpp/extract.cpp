#include<Rcpp.h>
#include"misc.h"
using namespace std;
using namespace Rcpp;

/* rm extract; gcc -O4 extract.c -o extract; ./extract craigslist-apa-data-bc-html-othermeta.csv
 note: should delete the html and otherAttributes folders before (re)running

 the program can use append mode for writing files, to catch records with same ID:
 see line: int duplicates = 0; // to ignore duplicates by taking latest record
*/

int go_to(FILE * f, const char * tag, size_t tag_len, char * buf, size_t * next, size_t * fp){
  if(*next == 0){
    *fp = ftell(f);  // if at start of match, record position
  }

  char c = fgetc(f);
  if(c != tag[(*next)++]){
    *next = 0;  // failed to match a char
    return 0;
  }
  else{
    // matched a char! 
    // printf("%c,next=%zu\n", c, *next);
  }

  if(*next == tag_len){
    *next = 0;  // if we matched the whole tag

    fseek(f, *fp, SEEK_SET);  // read stuff from match pos'n to confirm
    size_t br = fread(&buf[0], sizeof(char), tag_len, f);
    if(br != tag_len){
      printf("Err: br != tag_len\n");
      exit(1);
    }
    buf[tag_len] = '\0';  // printf("match: buf[%s]\n", buf);
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
  size_t fp = ftell(f); // return file to start of line. Where are we?
  if(fp == 0) return; // done if at beginning of file

  char c;
  do{
    c = fgetc2(f);
  }
  while(c != '\n');

  while(c == '\n' || c == '\r'){
    c = fgetc(f);
  }
  fseek(f, -1, SEEK_CUR); // go back one
}

//[[Rcpp::export]]
int extract(StringVector args){
  printf("extract()\n");

  int argc = args.size();
  if(argc != 1) err("extract [input csv filename]"); 

  // int main(int argc, char ** argv)
  int duplicates = 0;  // duplicates = 0: ignore duplicates by taking latest record, vs duplicates = 1
  int a = system("mkdir -p html");
  if(a != 0){
    err("command failed: mkdir -p html");
  }

  int debug = 0; // 1; // apply int debug=1; to print debug statements
  a = system("mkdir -p otherAttributes"); // some random stuff that was stuffed in next to the html, yikes!
  if(a != 0){
    err("command failed: mkdir -p otherAttributes");
  }

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

  string arg1(args[0]);
  const char * fn = arg1.c_str(); //argv[1];
  printf("check file size: %s\n", fn);
  size_t infile_size = file_size(fn); // file size
  printf("fopen(%s)\n", fn);

  FILE * f = fopen(fn, "rb");
  string t_f(arg1 + string("_tag"));
  string arg2;

  const char * tf;
  if(argc < 2){
    tf = t_f.c_str(); // strcat(argv[1], "_tag");
  }
  else{
    err("this option not supported");
    // allow an option to read from separate file, for parallelism case
    string a(args[1]);
    arg2.assign(a);
    tf = arg2.c_str(); // tf = argv[2];
  }

  printf("fopen2(%s)\n", tf);
  FILE * g = fopen(tf, "rb");
  if(!f){
    printf("\tfn: %s\n", fn);
    err("failed to open input file"); // the file itself
  }
  if(!g){
    printf("\tfn: %s\n", tf);
    err("failed to open start tag file *_tag: run find_start.c first"); // html start tag file
  }

  size_t n;
  char ** s = (char **) alloc(sizeof(char *));;
  *s = NULL;

  size_t i = 0;
  do{
    printf("\n---------------------------------------------------------------------------------------------\n");
    printf("gs()\n");
    n = gs(g, s);
    printf("end gs()\n");
    if(n < 1) break;

    size_t start_p;
    if(debug){
      printf("s[%s]\n", *s);
    }

    // the next five lines replace the statement: sscanf(*s, "%zu", &start_p);
    char * tmp1 = (char *)(void *) alloc(n + 1);
    for(int m = 0; m < n; m++) tmp1[m] = (*s)[m];
    tmp1[n] = '\0';
    sscanf(tmp1, "%zu", &start_p);
    free(tmp1);

    fseek(f, start_p, SEEK_SET);
    n = gs(f, s);

    // now find end tag
    next = 0;
    while(!go_to(f, end_tag, tag_len, buf, &next, &fp));

    // this is the span of the html
    if(debug){
      printf("\nstart_p %zu end_p %zu\n", start_p, fp + tag_len - 1);
    }

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

    string pre_s(string("html") + string(sep()));
    const char * pre = pre_s.c_str(); // "html/";
    char * t = (char *)(void *)alloc(strlen(pre) + strlen(id_s) + 1);
    strcpy(t, pre);
    strcpy(t + strlen(pre), id_s);
    t[strlen(pre) + strlen(id_s)] = '\0';

    // output file name
    FILE * h = fopen(t, duplicates?"ab":"wb");

    // secondary file to save otherAttributes string
    string pre_s2(string("otherAttributes") + string(sep()));
    cout << "pre_s2:[" << pre_s2 << "]" << endl;
    const char * pre2 = pre_s2.c_str(); // "otherAttributes/";
    char * t2 = (char *)(void *)alloc(strlen(pre2) + strlen(id_s) + 1);
    strcpy(t2, pre2);
    strcpy(t2 + strlen(pre2), id_s);
    t2[strlen(pre2) + strlen(id_s)] = '\0';
    if(debug){
      printf("\nofn:[%s]\n", t2);
    }
    FILE * j = fopen(t2, duplicates?"ab":"wb");

    // write html to file, here:
    size_t dat_sz = fp + tag_len - start_p;
    char * dat = (char *)(void *)alloc(dat_sz);

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
      // time_t t1; time(&t1);
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