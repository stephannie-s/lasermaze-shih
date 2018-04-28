#code for generating random laser tag board
#Python version: 3.5.0
import os, sys, getopt
path="/Users/stephshih/Documents/lasermaze-shih/"
os.chdir(path)
out_file=open("input files/test1.txt", "w")

import random
random.seed(37)
x_max=random.randint(0,1000)
y_max=random.randint(0,1000)
x_start=random.randint(0, x_max)
y_start=random.randint(0,y_max)
n_mirror=random.randint(0,1000)
x_mirror=list(range(x_max))
y_mirror=list(range(y_max))
random.shuffle(x_mirror)
random.shuffle(y_mirror)
mirrors_used=0
for i in range(0,1000):
    while mirrors_used<=n_mirror:
        if x_mirror 
