#April 28, 2108
#lasermaze
setwd("~/Documents/lasermaze-shih")
enteredfiles=commandArgs(trailingOnly = T)
if (length(enteredfiles)==0) {
  stop("incorrect number of files entered", call.=FALSE)
} else if (length(enteredfiles)==2) {
  name.in.file=enteredfiles[1] 
  outfile=enteredfiles[2] 
}
in.file=read.delim(name.in.file, header=F, sep=" ")
in.file[,3] = gsub(pattern='\\/', replacement='R', x=in.file[,3])
in.file[,3] = gsub(pattern='\\\\', replacement='L', x=in.file[,3])

#creating function for closest mirrors in relation to current position----
mirrors_north_south=function(x_value, y_value, counter,north){
  potential_y_values=mirrors[mirrors[,1]==x_value,]
  potential_y_values=potential_y_values[order(potential_y_values[,2]),]
  if (north==1){
    new_y_value=potential_y_values[potential_y_values[,2]>y_value,]
    counter=counter+abs(new_y_value[1,2]-y_value)
    if (dim(new_y_value)[1]>0){
      return(cbind(new_y_value[1,], 'N', counter))
    }
    else{return(NA)}
  }
  else{
    new_y_value=potential_y_values[potential_y_values[,2]<y_value,]
    counter=counter+abs(tail(new_y_value,n=1)[,2]-y_value)
    if (dim(new_y_value)[1]>0){
      return(cbind(tail(new_y_value,n=1),'S', counter))
    }
    else(return(NA))
  }
}
mirrors_east_west=function(x_value, y_value, counter,east){
  potential_x_values=mirrors[mirrors[,2]==as.numeric(y_value),]
  potential_x_values=potential_x_values[order(potential_x_values[,1]),]
  if (east==1){
    new_x_value=potential_x_values[potential_x_values[,1]>x_value,]
    counter=counter+abs(new_x_value[1,1]-x_value)
    if (dim(new_x_value)[1]>0){
      return(cbind(new_x_value[1,], 'E', counter))
    }
    else{return(NA)}
  }
  else{
    new_x_value=potential_x_values[potential_x_values[,1]<x_value,]
    counter=counter+abs(tail(new_x_value,n=1)[,1]-x_value)
    if (dim(new_x_value)[1]>0){
      return(cbind(tail(new_x_value, n=1),'W', counter))
    }
    else{return(NA)}
  }
}

#function to determine directionality----
directionfunct=function(coords){
  x_value=as.numeric(coords[1])
  y_value=as.numeric(coords[2])
  mirror_type=coords[3]
  direction=coords[4]
  counter=as.numeric(coords[5])
  if ((direction=="S" & mirror_type=="R")|(direction=='N' & mirror_type=='L')){coords=mirrors_east_west(x_value, y_value, counter, east=0)}
  if ((direction=="N" & mirror_type=="R")|(direction=='S' & mirror_type=='L')){coords=mirrors_east_west(x_value, y_value, counter, east=1)}
  if ((direction=="E" & mirror_type=="R")|(direction=='W' & mirror_type=='L')){coords=mirrors_north_south(x_value, y_value, counter, north=1)}
  if ((direction=="W" & mirror_type=="R")|(direction=='E' & mirror_type=='L')){coords=mirrors_north_south(x_value, y_value, counter, north=0)}
  return(coords)
}

#initialize maze----
x_max=in.file[1,1]
y_max=in.file[1,2]
mirrors=in.file[c(-1,-2),]
counter=0
x_value=in.file[2,1]
y_value=in.file[2,2]
direction=in.file[2,3]
if (direction=="W"){
  coords=mirrors_east_west(x_value, y_value, counter, east=0)
} else if (direction=="E"){
  coords=mirrors_east_west(x_value, y_value, counter, east=1)
} else if (direction=="N"){
  coords=mirrors_north_south(x_value, y_value, counter, north=1)
} else{
  coords=mirrors_north_south(x_value, y_value, counter, north=0)
}
counter=as.numeric(coords[5])

if (sum(is.na(coords))>0){
  end=3
  if (direction=="W"){
    counter=x_value
    final_coords=c(0,y_value)
  } else if (direction=="E"){
    counter=x_max-x_value-1
    final_coords=c(x_max-1,y_value)
  }else if (direction=="N"){
    counter=y_max-y_value-1
    final_coords=c(x_value,y_max-1)
  }else{
    counter=y_value
    final_coords=c(x_value,0)
  }
  cat(counter, file=outfile, sep="\n")
  cat(final_coords, file=outfile,append=T, sep=" ")
} else{end=0}

#Generating while statment to follow the laser----
process_record=as.data.frame(matrix(data=NA, nr=0, nc=4))
names(process_record)=c("X", "Y", "mirror", "direction")
names(coords)[c(-5)]=c("X", "Y", "mirror", "direction")
process_record=rbind(process_record, coords[-5])

while (end==0){
  coords=directionfunct(coords)
  if (sum(is.na(coords))>0){
    coords=tail(process_record, n=1)
    end=1
    }
  else if (dim(process_record)[1]==dim(unique(process_record[-5]))[1]){
    names(coords)[-5]=names(process_record)
    process_record=rbind(process_record, coords[-5])
    counter=coords[5]
  } 
  else {
     end=2
      cat(-1, file=outfile, sep="\n")
      }
  }

#compute final endpoint----
if (end==1){
  finalx=coords[1]
  finaly=coords[2]
  direction=coords[4]
  mirror_type=coords[3]
  if ((direction=="S" & mirror_type=="R")|(direction=='N' & mirror_type=='L')){
    counter=counter+finalx
    final_coords=cbind(0,finaly)
  } else if ((direction=="N" & mirror_type=="R")|(direction=='S' & mirror_type=='L')){
    counter=counter+x_max-finalx-1
    final_coords=cbind(x_max-1,finaly)
  } else if ((direction=="E" & mirror_type=="R")|(direction=='W' & mirror_type=='L')){
    counter=counter+y_max-finaly-1
    final_coords=cbind(finalx,y_max-1)
  } else if ((direction=="W" & mirror_type=="R")|(direction=='E' & mirror_type=='L')){
    counter=counter+finaly
    final_coords=cbind(finalx,0)
  }

  cat(unlist(counter), file=outfile, sep="\n")
  cat(unlist(final_coords), file=outfile,append=T, sep=" ")
}