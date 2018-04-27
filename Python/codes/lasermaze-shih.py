#python code for laser tag
#First addressing sample problem, then will address problems that do not hit a wall

#reading in input file
import os;
path="/Users/stephshih/Documents/lasermaze-shih/"
os.chdir(path)
in_file=open("input files/inputfile copy.txt", "r")

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
def mirrors_north(x_value, y_value,counter):
    potential_y_values=list(mirror_y_coord[i] for i in mirrors_same_axis(x_value, mirror_x_coord)) #make sure mirrors are on the same x axis
    mirror_type=list(mirror_direction[i] for i in mirrors_same_axis(x_value, mirror_x_coord))
    for yi in range(y_value+1,maze_size[1]):#if going north, want to check greater y values
        if yi in potential_y_values:
            new_y_value=yi
            adding_counts=abs(y_value-yi)
            mirror_type=mirror_type[potential_y_values.index(yi)]
            return(x_value, new_y_value,mirror_type,counter+adding_counts, "N")

def mirrors_south(x_value, y_value,counter):
    potential_y_values=list(mirror_y_coord[i] for i in mirrors_same_axis(x_value, mirror_x_coord))
    mirror_type=list(mirror_direction[i] for i in mirrors_same_axis(x_value, mirror_x_coord))
    for yi in range(y_value-1,-1,-1):#if going south, want to check decreasing y values
        if yi in potential_y_values:
            new_y_value=yi
            adding_counts=abs(y_value-yi)
            mirror_type=mirror_type[potential_y_values.index(yi)]
            return(x_value, new_y_value,mirror_type,counter+adding_counts, "S")
        

def mirrors_east(x_value, y_value,counter):
    potential_x_values=list(mirror_x_coord[i] for i in mirrors_same_axis(y_value, mirror_y_coord))
    mirror_type=list(mirror_direction[i] for i in mirrors_same_axis(y_value, mirror_y_coord))
    for xi in range(x_value+1,maze_size[0]):
        if xi in potential_x_values:
            new_x_value=xi
            adding_counts=abs(x_value-xi)
            mirror_type=mirror_type[potential_x_values.index(xi)]
            return(new_x_value, y_value,mirror_type,counter+adding_counts,"E")
    
def mirrors_west(x_value, y_value,counter):
    potential_x_values=list(mirror_x_coord[i] for i in mirrors_same_axis(y_value, mirror_y_coord))
    mirror_type=list(mirror_direction[i] for i in mirrors_same_axis(y_value, mirror_y_coord))
    for xi in range(x_value-1,-1,-1):
         if xi in potential_x_values:
            new_x_value=xi
            adding_counts=abs(x_value-xi)
            mirror_type=mirror_type[potential_x_values.index(xi)]
            return(new_x_value, y_value,mirror_type,counter+adding_counts, "W")

#create function to determine directionality
def directionfunct(x_value, y_value,mirror_type, counter, direction):
    if (direction=="S" and mirror_type=="R") or (direction=="N" and mirror_type=="L"):
        new_coords=mirrors_west(x_value,y_value,counter)
    elif (direction=="N" and mirror_type=="R") or (direction=="S" and mirror_type=="L"):
        new_coords=mirrors_east(x_value,y_value,counter)
    elif (direction=="E" and mirror_type=="R") or (direction=="W" and mirror_type=="L"):
        new_coords=mirrors_north(x_value,y_value,counter)
    elif (direction=="W" and mirror_type=="R") or (direction=="E" and mirror_type=="L"):
        new_coords=mirrors_south(x_value,y_value,counter)
    return(new_coords)       

               
        
##initialize maze to find very first mirror
counter=0
direction=starting_point[2]
x_value=int(starting_point[0])
y_value=int(starting_point[1])
if (direction=="W"):
    new_coords=mirrors_west(x_value,y_value,counter)
elif (direction=="E"):
    new_coords=mirrors_east(x_value,y_value,counter)
elif (direction=="N"):
    new_coords=mirrors_north(x_value,y_value,counter)
elif (direction=="S"):
    new_coords=mirrors_south(x_value,y_value,counter)

x_value=new_coords[0]
y_value=new_coords[1]
mirror_type=new_coords[2]
counter=new_coords[3]
direction=new_coords[4]

##while statement to continue
end=0
process_record=[]
while end==0:
    new_coords=directionfunct(x_value, y_value, mirror_type, counter,direction)
    if new_coords is not None:
        process_record.append(new_coords)
        x_value=new_coords[0]
        y_value=new_coords[1]
        mirror_type=new_coords[2]
        counter=new_coords[3]
        direction=new_coords[4]
    else:
        end=1

#compute final endpoint, this should be the very last entry
if (direction=="S" and mirror_type=="R") or (direction=="N" and mirror_type=="L"):
    counter+=x_value
    final_coords=[0,y_value]
elif (direction=="N" and mirror_type=="R") or (direction=="S" and mirror_type=="L"):
    counter+=maze_size[0]-x_value-1
    final_coords=[0,y_value]
elif (direction=="E" and mirror_type=="R") or (direction=="W" and mirror_type=="L"):
    counter+=maze_size[1]-y_value
    final_coords=[x_value,0]
elif (direction=="W" and mirror_type=="R") or (direction=="E" and mirror_type=="L"):
    counter+=y_value
    final_coords=[x_value,0]


out_file=open("output files/inputfile copy.txt", "w")
out_file.write(str(counter)+"\n")
for i in final_coords:
    out_file.write(str(i)+" ")
out_file.close()
        
