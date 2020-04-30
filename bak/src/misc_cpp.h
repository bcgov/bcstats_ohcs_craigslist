#include<map>
#include<set>
#include<string>
#include<vector>
#include<time.h>
#include<cctype>
#include<locale>
#include<stdio.h>
#include<fstream>
#include<iterator>
#include<iostream>
#include<stdlib.h>
#include<memory.h>
#include<string.h>
#include<sstream>
#include<algorithm>

using namespace std;

#define str string
#define for0(x, n) for(x = 0; x < n; x++)

// error message
void err(const char * msg){
  printf("Error: %s\n", msg);
  exit(1);
}

FILE * wopen(string fn){
  FILE * f = fopen(fn.c_str(), "wb");
  if(!f) err("failed to open file for writing");
  return f;
}

// allocate memory
void * alloc(size_t nb){
  void * d = malloc(nb);
  if(!d){
    printf("%zu\n", nb);
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
    // printf("%c", c);
    n++;
    c = fgetc(f);
  }
  size_t fp2 = ftell(f);  // printf("\nn %zu\n", n);

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

/* split a string (a-la python) */
vector<string> split(string s, char delim){
  trim(s);
  bool extra = (s[s.size() - 1] == delim);
  std::vector<std::string> ret;
  std::istringstream iss(s);
  std::string token;
  while(getline(iss,token,delim)) ret.push_back(token);

  if(extra) ret.push_back(str(""));
  return ret;
}

/* split a string (a-la python) */
vector<string> split(string s){
  trim(s);
  const char delim = ',';
  bool extra = (s[s.size() -1] == delim);

  std::vector<std::string> ret;
  std::istringstream iss(s);
  string token;
  while(getline(iss,token,delim)) ret.push_back(token);

  vector<string>::iterator it;
  for(it = ret.begin(); it != ret.end(); it++){
    trim(*it);
  }
  if(extra) ret.push_back(str(""));
  return ret;
}

