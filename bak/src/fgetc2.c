// gcc fgetc2.c; ./a.out 
#include<stdio.h>
#include<stdlib.h>

char fgetc2(FILE * f){
  fseek(f, -1, SEEK_CUR);
  char c = fgetc(f);
  fseek(f, -1, SEEK_CUR);
  return c;
}

int main(int argc, char ** argv){
  FILE * f = fopen("tmp.txt", "wb");
  fprintf(f, "hello1234");
  fclose(f);

  f = fopen("tmp.txt", "rb");
  size_t end = 9;
  fseek(f, end, SEEK_SET);

  for(size_t i = 0; i < end; i++){
    printf("[%c]\n", fgetc2(f));
  }
  return 0;
}
