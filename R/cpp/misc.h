#ifndef _MISC_H_
#define _MISC_H_

#include<time.h>
#include<stdio.h>
#include<map>
#include<set>
#include<vector>
#include<string>
#include<sstream>
#include<fstream>
#include<stdlib.h>
#include<limits.h>
#include<memory.h>
#include<iostream>
#include<algorithm>

#include <stdio.h> /* defines FILENAME_MAX */
#ifdef WINDOWS
#include <direct.h>
#define _cwd _getcwd
#else
#include <unistd.h>
#define _cwd getcwd
#endif

using namespace std;

#define str string

/* shorthand for for loops from 0 to N */
#define for0(i,n) for(i = 0; i < n; i++)

#define STR_MAX 16384

#define mtx_lock pthread_mutex_lock
#define mtx_unlock pthread_mutex_unlock

void rewind(ifstream &a);

#define str string
string cwd();

// error message
void err(const char * msg){
  printf("Error: %s\n", msg);
  exit(1);
}

void err(string msg);

/* split a string (a-la python) */
vector<string> split(string s, char delim);
vector<string> split(string s); // comma
vector<string> split_special(string s); // comma with possible commas inside quotation marks!
string join(const char * delim, vector<string> s);

template<class T> std::ostream& operator << (std::ostream& os, const std::vector<T>& v){
  os << "[";
  for (typename std::vector<T>::const_iterator ii = v.begin(); ii != v.end(); ++ii){
    os << " '" << *ii << "'";
  }
  os << "]";
  return os;
}

template<class T> std::ostream& operator << (std::ostream& os, const std::set<T>& v){
  os << "{";
  for (typename std::set<T>::const_iterator ii = v.begin(); ii != v.end(); ++ii){
    os << " " << *ii;
  }
  os << "}";
  return os;
}

template<class A, class B> std::ostream& operator << (std::ostream& os, const std::map<A, B>& v){
  os << "{" << endl;
  for (typename std::map<A, B>::const_iterator ii = v.begin(); ii != v.end(); ++ii){
    os << ii->first << ":" << ii->second << ","; //endl;
  }
  os << "}" << endl;
  return os;
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

#include <cctype>
#include <locale>

//a trim from start (in place)
static inline void ltrim(std::string &s){
  s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch){
    return !std::isspace(ch);
  }
  ));
}

// trim from end (in place)
static inline void rtrim(std::string &s){
  s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch){
    return !std::isspace(ch);
  }
  ).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s){
  ltrim(s);
  rtrim(s);
}

// trim from start (copying): not implemented properly
static inline std::string ltrim_copy(std::string s){
  ltrim(s);
  return s;
}

// trim from end (copying): not implemented properly
static inline std::string rtrim_copy(std::string s){
  rtrim(s);
  return s;
}

// trim from both ends (copying): not implemented properly
static inline std::string trim_copy(std::string s){
  trim(s);
  return s;
}

static inline void trim(std::string &s, char delim){
  str ret("");
  int end = s.size() - 1;
  int start = 0;
  while(s[start] == delim) start += 1;
  while(s[end] == delim) end -= 1;
  s = s.substr(start, 1 + end - start);
}

#define strip trim

/* convert to lower case */
static inline void lower(std::string & s){
  std::transform(s.begin(), s.end(), s.begin(), ::tolower);
}

static inline std::string lower_copy(std::string &s){
  string r(s);
  std::transform(r.begin(), r.end(), r.begin(), ::tolower);
  return r;
}

void prints(char * s, size_t n){
  for(size_t i = 0; i < n; i++){
    printf("%c", s[i]);
  }
}

/* get line: from current fpos, until newline / end.
dynamic memory allocation: allocates it's own memory
but free existing variable first if needed */
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
  char * buf = (char *) (void *) alloc(n + 1);
  fseek(f, fp, SEEK_SET);
  for(size_t i = 0; i < n; i++){
    c = fgetc(f);
    buf[i] = c;
  }
  buf[n] = '\0'; // don't forget null-term
  *b = buf;

  // get ready for next non-nothing
  fseek(f, fp2, SEEK_SET);
  while(c == '\n' || c == '\r'){
    c = fgetc(f); // forward over line delimiter
  }
  return n;
}

/* get size of file pointer */
size_t size(FILE * f);
size_t fsize(string fn);

bool exists(string fn);

// in-memory reader (writer to be implemented)
// note this should be able to modulate between available protocols (like ifstream,
// ofstream, etc. , fwrite, fread, if available)

FILE * wopen(string fn);

size_t file_size(const char * fn){
  FILE * f = fopen(fn, "rb");
  if(!f) err("failed to open file");
  fseek(f, 0L, SEEK_END);
  size_t s = ftell(f);
  fclose(f);
  return s;
}

class mfile{
  FILE * fp;
  char * d;
  size_t fs;
  char s_bf[STR_MAX];
  char c;

  size_t l_pos; // position of start of current line
  size_t c_pos; // present read position within line

  //T x; // just using this to trick the compiler to let us implement the class in the header!
  public:

  mfile(string f_n, char * mode);
  int getline(string & buf);
  void rewind();
  void close();

  clock_t start_t, last_t;
  size_t last_pos;
  size_t tellg();
  size_t len();
  void status();

  };

  /* function to produce a distributed map of finite trajectory generation, with information-theoretically optimal compression */
  // this requires "class SA" (list / map hybrid)
  //
  // use this to algebraically encode e.g. lists of filenames in the format: msp2000-17, for continuous times..
  // e.g, [ab, ac] --> a[b,c]
  // [abc, ac] --> a[b[c],c]
  //
  //
  //

// float-int tuple for sorting distances
class f_i{
  public:
  float f;
  size_t i;
  f_i(float g = 0., size_t h = 0){
    // constructor. 0-index is null
    f = g;
    i = h;
  }
  f_i(const f_i &a){
    // copy constructor
    f = a.f;
    i = a.i;
  }
};

bool operator < (const f_i &a, const f_i &b);

/*

// float-int tuple for sorting distances
class f_ij{
  public:
  float f;
  size_t i,j;
  f_ij(float f_ =0, size_t i_=0, size_t j_=0){
    // constructor. 0-index is null
    f = f_;
    i = i_;
    j = j_;
    cout << " fij(" << f << "," << i << "," << j << ")" << endl;
  }
  f_ij(const f_ij &a){
    // copy constructor
    f = a.f;
    i = a.i;
    j = a.j;
   cout << "*fij(" << f << "," << i << "," << j << ")" << endl;
  }
};

bool operator < (const f_ij &a, const f_ij &b);
*/

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
#endif
