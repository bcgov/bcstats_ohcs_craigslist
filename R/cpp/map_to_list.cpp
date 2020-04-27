/* got this from stackoverflow.com. Might need this later! */

#include <Rcpp.h>
// [[Rcpp::export]]
Rcpp::List map_to_list(Rcpp::CharacterVector cv, Rcpp::NumericVector nv) {
  std::map<std::string, double> my_map;

  for (R_xlen_t i = 0; i < cv.size(); i++) {
    my_map.insert(std::make_pair(Rcpp::as<std::string>(cv[i]), nv[i]));
  }

  Rcpp::List my_list(my_map.size());
  Rcpp::CharacterVector list_names(my_map.size());
  std::map<std::string, double>::const_iterator lhs = my_map.begin(), rhs = my_map.end();

  for (R_xlen_t i = 0; lhs != rhs; ++lhs, i++) {
    my_list[i] = lhs->second;
    list_names[i] = lhs->first;
  }

  my_list.attr("names") = list_names;
  return my_list;
}

/*** R
.names <- letters[1:20]
.values <- rnorm(20)

(res <- map_to_list(.names, .values))
#$a
#[1] -0.8596328

#$b
#[1] 0.1300086

#$c
#[1] -0.1439214

#$d
#[1] -1.017546

## etc... */
