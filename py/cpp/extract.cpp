#include"misc.h"
using namespace std;

/* rm extract; gcc -O4 extract.c -o extract; ./extract craigslist-apa-data-bc-html-othermeta.csv
note: should delete the html and otherAttributes folders before (re)running

the program can use append mode for writing files, to catch records with same ID:
see line: int duplicates = 0; // to ignore duplicates by taking latest record
*/

int go_to(FILE * f, const char * tag, size_t tag_len, char * buf, size_t * next, size_t * fp){
  if(*next == 0){
    *fp = ftell(f); // if at start of match, record position
  }

  char c = fgetc(f);
  if(c != tag[(*next)++]){
    *next = 0; // failed to match a char
    return 0;
  }
  else{
    // matched a char!
    // printf("%c,next=%zu\n", c, *next);
  }

  if(*next == tag_len){
    *next = 0; // if we matched the whole tag

    fseek(f, *fp, SEEK_SET); // read stuff from match pos'n to confirm
    size_t br = fread(&buf[0], sizeof(char), tag_len, f);
    if(br != tag_len){
      printf("Err: br != tag_len\n");
      exit(1);
    }
    buf[tag_len] = '\0'; // printf("match: buf[%s]\n", buf);
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

size_t extract(string arg){
  printf("extract()\n");

  // int main(int argc, char ** argv)
  int duplicates = 0; // duplicates = 0: ignore duplicates by taking latest record, vs duplicates = 1
  int debug = 0; // 1; // apply int debug=1; to print debug statements

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

  const char * fn = arg.c_str(); //argv[1];
  if(debug) printf("check file size: %s\n", fn);
  size_t infile_size = file_size(fn); // file size
  if(debug) printf("fopen(%s)\n", fn);

  FILE * f = fopen(fn, "rb");
  string t_f(arg + string("_tag"));
  const char * tf  = t_f.c_str(); // strcat(argv[1], "_tag");

  if(debug) printf("fopen2(%s)\n", tf);
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

  FILE * log_f = fopen("extract_log.txt", "wb");

  size_t i = 0;
  do{
    n = gs(g, s);
    if(n < 1) break;

    size_t start_p;
    if(debug){
      printf("s[%s]\n", *s);
    }

    // the next five lines replace the statement: sscanf(*s, "%zu", &start_p);
    char * tmp1 = (char *)(void *) alloc(n + 1);
    for(size_t m = 0; m < n; m++) tmp1[m] = (*s)[m];
    tmp1[n] = '\0';
    sscanf(tmp1, "%zu", &start_p);
    free(tmp1);

    fseek(f, start_p, SEEK_SET);
    n = gs(f, s);

    // now find end tag
    next = 0;
    while(!go_to(f, end_tag, tag_len, buf, &next, &fp)){
    }

    // this is the span of the html
    if(debug){
      printf("start_p %zu end_p %zu\n", start_p, fp + tag_len - 1);
    }

    fprintf(log_f, "start_p %zu end_p %zu\n", start_p, fp + tag_len - 1);

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
    // cout << "pre_s2:[" << pre_s2 << "]" << endl;
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

    if(nr != nw){
      printf("nr %zu\n", nr);
      printf("nw %zu\n", nw);
      printf("t %s\n", t);
      err("write fail");
    }
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
    fwrite(*s, sizeof(char), strlen(*s), j);
    fclose(j);

    i += 1;
    if(i% 111 == 0){
      double frac = 100. * (double)fp / (double)infile_size;
      // time_t t1; time(&t1);
      double dt = (double)(clock() - c0) / (double) CLOCKS_PER_SEC; // (float)t1 - (float)t0;
      double nps = (double)fp / (double)dt;
      double eta = (double)((double)infile_size - (double)fp) / (double)nps;
      int pct = (int)ceil(frac);
      printf(" %%%d +w %s eta: %e s i=%zu\n", pct, t, eta, i );
    }
    free(t);
  }
  while(n > 0);

  fclose(f);
  fclose(g);

  fclose(log_f);
  // end program
  free(*s);

  time_t t1;
  time(&t1);
  printf("dt %fs\n", (float)(t1 - t0));
  printf("n_extract %zu\n", i);
  return 0;
}

int main(int argc, char ** argv){
  if(argc < 2) err("extract.cpp [html file name]");
  extract(string(argv[1]));
  exit(0);
}

