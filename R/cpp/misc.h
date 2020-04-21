#include<time.h>
#include<stdio.h>
#include<vector>
#include<string>
#include<fstream>
#include<stdlib.h>
#include<memory.h>
#include<iostream>

using namespace std;

#define str string

// error message
void err(const char * msg){
  printf("Error: %s\n", msg);
  exit(1);
}

// allocate memory
void * alloc(size_t nb){
  // printf("alloc(%zu)\n", nb);
  void * d = malloc(nb);
  if(!d){
    printf("bytes requested: %zu\n", nb);
    err("failed to allocate memory");
  }
  memset(d, '\0', nb);
  return d;
}

void prints(char * s, size_t n){
  for(size_t i = 0; i < n; i++){
    printf("%c", s[i]);
  }
}

/* get line: from current fpos, until newline / end.
* Dynamic memory allocation: allocates it's own memory
* but frees existing variable at location first if needed*/
size_t gs(FILE * f, char ** b){
  // clear buffer if exists
  if(*b != NULL) free(*b);

  size_t n = 0; // number of chars found
  size_t fp = ftell(f);
  char c = fgetc(f);
  while(c != EOF && c != '\n' && c != '\r'){
    //printf("%c ", c);
    n++;
    c = fgetc(f);
  }
  size_t fp2 = ftell(f);
  //printf("\nn %zu\n", n);

  // allocate as much memory as we need
  char * buf = (char *) (void *) alloc(n);
  fseek(f, fp, SEEK_SET);
  for(size_t i = 0; i < n; i++){
    c = fgetc(f);
    buf[i] = c;
  }
  *b = buf;

  // get ready for next non-nothing
  fseek(f, fp2, SEEK_SET);
  while(c == '\n' || c == '\r'){
    c = fgetc(f); // forward over line delimiter
  }
  return n;
}

size_t file_size(const char * fn){
  FILE * f = fopen(fn, "rb");
  if(!f) err("failed to open file");
  fseek(f, 0L, SEEK_END);
  size_t s = ftell(f);
  fclose(f);
  return s;
}

inline char separator(){
  #if defined _WIN32 || defined WIN32 || defined __CYGWIN__
    return '\\';
  #else
    return '/';
  #endif
}

const char * sep(){
  char c[2];
  c[0] = separator();
  c[1] = '\0';
  string s(&c[0]);
  return s.c_str();
}


