#lasermaze generate input file
setwd("~/Documents/lasermaze-shih/input files/")
set.seed(37)
sample.size=20
x_max=sample(c(1:sample.size),size=1)
y_max=sample(c(1:sample.size),size=1)
n_mirror=sample(c(1:x_max*y_max-1),size=1) #maximum number of mirrors is the area -1 for the starting position
x_values=sample(c(1:x_max),size=n_mirror*5,replace=T)-1
y_values=sample(c(1:y_max),size=n_mirror*5,replace=T)-1
coordinates=unique(paste(x_values, y_values, sep=" "))
mirror_direction=sample(c("\\", "/"), size=length(coordinates), replace=T)
mirror_direction[1]=sample(c("N", "S","E", "W"), size=1)
coordinates=paste(coordinates, mirror_direction, sep=" ")
use_coordinates=coordinates[c(0:n_mirror+1)]
cat(paste(x_max, y_max, sep=" "),file="largeoutfile.txt",sep="\n")
cat(use_coordinates,file="largeoutfile.txt",sep="\n",append=TRUE)
