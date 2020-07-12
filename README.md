# bcstats ohcs craigslist
Extractor / parser, written for web-scraped craigslist data as provided to BC Stats, by Harmari Inc.

**Instructions**
1. Install R 4.0.0, Rtools and RStudio first (make sure your environment variable:
Path 
is modified to include your rtools folder. I added
;C:\rtools40
to the end of my Path variable). How to change the Path variable? Control panel -> System -> Advanced system settings -> Environment Variables
2. Open RStudio in administrator mode and select: session-> set working directory --> to Source location (for R/setup.R / R/run.R)
3. (first time only) Open R/setup.R
4. (first time only) Select all lines of R/setup.R and run (alternately, could run by
Rscript setup.R # from Terminal within RStudio, supposing Terminal is pointed to the R folder)
5. Open R/run.R, select all lines and run (alternately, could run by 
Rscript run.R # from Terminal within Rstudio, supposing Terminal is pointed to the R folder)
6. (first time only) If you're prompted to download additional stuff, may need to say yes
* N.B., the data must be in the same folder as the source code
* N.B.N.B may need to modify new input data file names so there aren't any collisions

**Overview**

Use some large data / HPC-ish techniques to wrangle a large, irregular housing-market dataset on an ordinary computer, in a finite amount of time
* out of memory
* parallelism

The data include an irregularly formatted CSV file (22GB) incl. approx. 1 million HTML files stuffed into the CSV, where each HTML-file attribute, spans approx. 500 lines. Python 3's "import csv" and R's "library{vroom}" weren't able to read the data at this time, so custom out-of-memory slicing was developed. Moreover, Python3's BeautifulSoup html-parsing, was applied and accelerated using full machine-parallelism

The data contain sensitive information and will not be posted, however project documentation will be included when approved

## Process analytics
Sample visualization of process monitor for one of the steps in this "big-data" application
![Process analytics](img/process_analytics.jpg)

## License

Copyright 2020 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
