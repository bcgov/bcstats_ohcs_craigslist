#include"misc.h"

int main(int argc, char ** argv){
  long unsigned int n_error = 0;

  if(argc < 2){
    cout << "csv_split.cpp: split csv into columnar sets\n";
    err("usage:\n\tcsv_split.cpp [input file to split]");
  }
  string f_n(argv[1]);
  ifstream t(f_n);
  string s;

  int error;
  unsigned int i;
  FILE ** f = NULL;  // output files
  str newline("\n");
  vector<string> words;  // comma delimited chunks
  unsigned int n_f = 0;  // number of fields
  vector<string> field_names;  // names of the fields
  long unsigned int l_i = 0;  // line index

  while(getline(t,s)){
    error = false;
    words = split(s);

    if(l_i == 0){
      field_names = words;
      n_f = words.size();

      /* open a file for each field */
      f = (FILE **) alloc(sizeof(FILE *) * n_f);

      for0(i, n_f){
        str field_name(words[i]);
        std::replace(field_name.begin(), field_name.end(),'.', '_');
        str result("");
	std::remove_copy(field_name.begin(), field_name.end(), std::back_inserter(result), '*');
	field_name = result;
        string fn_i(string(f_n) + string("_") + field_name);
        cout << " +w " << fn_i << endl;
        f[i] = wopen(fn_i);
      }
      cout << "field_names: " << field_names << endl;
    }
    else{
      if(words.size() != n_f){
        cout << " l_i " << l_i << " " << words.size();
        cout <<	" n_f=" << n_f << " expected=" << words.size() << " " << words << endl;
        error = true;
        n_error ++;
        // exit(1);  (should this be commented out?)
      }
    }

    if(!error){
      for0(i, n_f){
        const char * word;

	if(l_i == 0){
          str field(words[i]);
          std::replace(field.begin(), field.end(), '.', '_');
          str result("");
          std::remove_copy(field.begin(), field.end(), std::back_inserter(result), '*');
          words[i] = result;
        }
        else{
          fprintf(f[i], "\n");
        }
        word = words[i].c_str();
        fwrite(word, strlen(word), 1, f[i]);
      }
    }

    if((++l_i) % 1000000 == 0){
      cout << words << endl;
    }
  }
  t.close();
  for0(i, n_f){
    fclose(f[i]);
  }
  cout << "n_error " << n_error << endl;
  cout << "done" << endl;
  return 0;
}
