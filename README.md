Code for solving the laser maze problem

NOTE: Please use Python version 3.5.x or 3.6.x as you may get different results using version 2.7

To run the Python code (lasermaze-shih.py) through command line:
Python3 Python/codes/lasermaze-shih.py ./path/to/input/file ./path/to/output/file

To run the R code (lasermaze-shih.R) through command line:
Rscript R/codes/lasermaze-shih.R ./path/to/input/file ./path/to/output/file

Folders:
1) Input files: Includes all the tested input files. See below for more information.
2) Python: Includes a folder with codes and a separate folder with output files corresponding to each input file 
3) R: Includes a folder with codes and a separate folder with output files corresponding to each input file 

Input files:
These are various input files tested using the Python and R codes. 
1) example.txt : This is to replicate the example given by the challenge
2) example_2.txt: Testing if no mirrors are hit, using grid from example.txt
3) example_3.txt: Testing laser going east hitting ‘/‘ mirror, using grid from example.txt
4) example_4.txt: Testing laser going north hitting ‘\’ mirror and laser going west hitting ‘\’ mirror, using grid from example.txt
5) example2.txt: Testing laser going west hitting ‘/‘ and going north hitting ‘/‘
6) loop.txt: This is to test an example with a laser that never hits a wall
7) greaterloop.txt: This is to use test another example with a laser that never hits a wall
8) nomirror.txt: This is to test results with no mirror
