**Instructions for R version**
1. Install R 4.0.0, Rtools and RStudio first (make sure your environment variable:
Path 
is modified to include your rtools folder. I added
;C:\rtools40
to the end of my Path variable). How to change the Path variable? Control panel -> System -> Advanced system settings -> Environment Variables
2. Open RStudio in administrator mode and select: session-> set working directory --> to Source location (for R/setup.R / R/run.R)
3. (first time only) Open R/setup.R
4. (first time only) Select all lines of R/setup.R and run (alternately, could run by
Rscript setup.R # from Terminal within RStudio, supposing Terminal is pointed to the R folder; this method seems to perform better)
5. Open R/run.R, select all lines and run (alternately, could run by 
Rscript run.R # from Terminal within Rstudio, supposing Terminal is pointed to the R folder; this method seems to perform better)
6. (first time only) If you're prompted to download additional stuff, may need to say yes
* N.B., the data must be in the same folder as the source code (the R/ subfolder folder)
* N.B.N.B may need to modify new input data file names in order to avoid collisions

**How to add QA entries for data updates**
(to be completed)
