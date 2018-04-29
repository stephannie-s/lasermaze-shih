#python code for laser tag
#Python version: 3.5.0 or 3.6.5

#reading in input file
import os, sys, getopt
files=getopt.getopt(sys.argv[1:],'')
in_file=open(files[1][0], 'r')
out_file=open(str(files[1][1]),'w')

maze_size=in_file.readline().strip("\n").split(" ")
maze_size=[int(i) for i in maze_size]
starting_point=in_file.readline().strip("\n").split(" ")
mirror_x_coord=[]
mirror_y_coord=[]
mirror_direction=[]
for line in in_file:
    splitting=line.strip("\n").split(" ")
    mirror_x_coord.append(int(splitting[0]))
    mirror_y_coord.append(int(splitting[1]))
    if splitting[2]=='/':
        mirror_direction.append("R")
    else:
        mirror_direction.append("L")

#create a function that looks for multiple mirrors on the same axis
def mirrors_same_axis(coord_value, interested_axis):
    keeping_values=[]
    for ik in range(0,len(interested_axis)):
        if interested_axis[ik]==coord_value:
            keeping_values.append(ik)
    return(keeping_values)

#create function to check for the first mirrors in relation to current position
def mirrors_north_south(x_value, y_value,counter,north):
    potential_y_values=[]
    potential_mirror_type=[]
    for i in mirrors_same_axis(x_value, mirror_x_coord):
        potential_y_values.append(mirror_y_coord[i])#make sure mirrors are on the same x axis
        potential_mirror_type.append(mirror_direction[i])
    if north==1:
        for yi in range(y_value+1,maze_size[1]+1):#if going north, want to check greater y values
            if yi in potential_y_values:
                new_y_value=yi
                adding_counts=abs(y_value-yi)
                mirror_type=potential_mirror_type[potential_y_values.index(yi)]
                return(x_value, new_y_value,mirror_type,"N",counter+adding_counts)
    else:
        for yi in range(y_value-1,-1,-1):#if going south, want to check decreasing y values
            if yi in potential_y_values:
                new_y_value=yi
                adding_counts=abs(y_value-yi)
                mirror_type=potential_mirror_type[potential_y_values.index(yi)]
                return(x_value, new_y_value,mirror_type,"S",counter+adding_counts)
        

def mirrors_east_west(x_value, y_value,counter,east):
    potential_x_values=[]
    potential_mirror_type=[]
    for i in mirrors_same_axis(y_value, mirror_y_coord):
        potential_x_values.append(mirror_x_coord[i])
        potential_mirror_type.append(mirror_direction[i])
    if east==1:
        for xi in range(x_value+1,maze_size[0]+1):
            if xi in potential_x_values:
                new_x_value=xi
                adding_counts=abs(x_value-xi)
                mirror_type=potential_mirror_type[potential_x_values.index(xi)]
                return(new_x_value, y_value,mirror_type,"E",counter+adding_counts)
    else:
        for xi in range(x_value-1,-1,-1):
             if xi in potential_x_values:
                new_x_value=xi
                adding_counts=abs(x_value-xi)
                mirror_type=potential_mirror_type[potential_x_values.index(xi)]
                return(new_x_value, y_value,mirror_type, "W",counter+adding_counts)

#create function to determine directionality
def directionfunct(x_value, y_value,mirror_type,  direction,counter):
    if (direction=="S" and mirror_type=="R") or (direction=="N" and mirror_type=="L"):
        coords=mirrors_east_west(x_value,y_value,counter, east=0)
    elif (direction=="N" and mirror_type=="R") or (direction=="S" and mirror_type=="L"):
        coords=mirrors_east_west(x_value,y_value,counter, east=1)
    elif (direction=="E" and mirror_type=="R") or (direction=="W" and mirror_type=="L"):
        coords=mirrors_north_south(x_value,y_value,counter, north=1)
    elif (direction=="W" and mirror_type=="R") or (direction=="E" and mirror_type=="L"):
        coords=mirrors_north_south(x_value,y_value,counter, north=0)
    return(coords)       

               
        
#initialize maze to find very first mirror
counter=0
direction=starting_point[2].upper()
x_value=int(starting_point[0])
y_value=int(starting_point[1])
if (direction=="W"):
    new_coords=mirrors_east_west(x_value,y_value,counter,east=0)
elif (direction=="E"):
    new_coords=mirrors_east_west(x_value,y_value,counter, east=1)
elif (direction=="N"):
    new_coords=mirrors_north_south(x_value,y_value,counter,north=1)
elif (direction=="S"):
    new_coords=mirrors_north_south(x_value,y_value,counter, north=0)

if new_coords is not None:
    x_value=new_coords[0]
    y_value=new_coords[1]
    mirror_type=new_coords[2]
    direction=new_coords[3]
    counter=new_coords[4]
    end=0
else:
    end=3
    if direction=="W":
        counter=x_value
        final_coords=[0,y_value]
    elif direction=="E":
        counter=maze_size[0]-x_value-1
        final_coords=[maze_size[0]-1,y_value]
    elif direction=="N":
        counter=maze_size[1]-y_value-1
        final_coords=[x_value,maze_size[1]-1]
    elif direction=="S":
        counter=y_value
        final_coords=[x_value,0]
    out_file.write(str(counter)+"\n")
    for i in final_coords:
        out_file.write(str(i)+" ")
    out_file.close()


#while statement to continue
process_record=[]
while end==0:
    new_coords=directionfunct(x_value, y_value, mirror_type,direction, counter)
    if len(process_record)==len(set(process_record)) and new_coords is not None:
            process_record.append(new_coords[:4])
            x_value=new_coords[0]
            y_value=new_coords[1]
            mirror_type=new_coords[2]
            direction=new_coords[3]
            counter=new_coords[4]
    else:
        if len(process_record)>len(set(process_record)):
            end=2
            out_file.write("-1\n")
            out_file.close()
        else:
            end=1
        
#compute final endpoint, this should be the very last entry
if end==1:
    if (direction=="S" and mirror_type=="R") or (direction=="N" and mirror_type=="L"):
        counter+=x_value
        final_coords=[0,y_value]
    elif (direction=="N" and mirror_type=="R") or (direction=="S" and mirror_type=="L"):
        counter+=maze_size[0]-x_value-1
        final_coords=[maze_size[0]-1,y_value]
    elif (direction=="E" and mirror_type=="R") or (direction=="W" and mirror_type=="L"):
        counter+=maze_size[1]-y_value-1
        final_coords=[x_value,maze_size[1]-1]
    elif (direction=="W" and mirror_type=="R") or (direction=="E" and mirror_type=="L"):
        counter+=y_value
        final_coords=[x_value,0]
    if final_coords is not None:
        out_file.write(str(counter)+"\n")
        for i in final_coords:
            out_file.write(str(i)+" ")
        out_file.close()


        
