import game_engine
import random
from collections import Counter
import math

class memory():
    def __init__(self, value,gold=0,wood=0,food=0,inh=10,used_inh=0):
        self.value=value
        self.gold=gold
        self.wood=wood
        self.food=food
        self.inh=inh
        self.used_inh=used_inh
        self.busy_buildings=[]
        self.busy_farms=[]
mem=memory(3,0,0,50,10,0)


def initialize_grids(grids):
    c=game_engine.Col()
    grids.append(game_engine.Grid(40,60,position=[15,50],colors=[c.blue,c.white,c.darkgreen,c.yellow,c.brown,c.grey,c.red,c.darkgreen]))
    terrains=[1]
    grids[0].generate_random_map(terrains)
    grids.append(game_engine.Grid(5,1,position=[1300,50],cell_size=[200,50],margin=5,colors=[c.grey,c.green]))
    grids.append(game_engine.Grid(5,1,position=[1300,325],cell_size=[200,50],margin=5,colors=[c.grey,c.green]))   
    grids.append(game_engine.Grid(5,1,position=[1300,600],cell_size=[200,50],margin=5,colors=[c.white]))
    return(grids)

def initialize_labels(labels):
    menu1=["Build a house (200)","Build a woodcutter (500)", "Build a farm (1000)", "", ""]
    for i in range(len(menu1)):    
        labels.append(game_engine.Label([1320,70+55*i],menu1[i],fontsize=15))
        
    menu2=["Reset","","","100 Food->1 Inhabitant",""]
    for i in range(len(menu2)):    
        labels.append(game_engine.Label([1320,345+55*i],menu2[i],fontsize=15))
 

    menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Inhabitants: "+str(mem.inh-mem.used_inh)+"/"+str(mem.inh)]    
    for i in range(len(menu3)):    
        labels.append(game_engine.Label([1320,620+55*i],menu3[i],fontsize=15))
        
    return(labels)

def evaluate_click(grids,click):
    map_grids=[grids[0]]
    menu_grids=[grids[1],grids[2]]
    for grid in map_grids:
        row,column=grid.evaluate_row_column_indices(click)
        set_element_value(grid,row,column,mem.value)  
        #print("Click ", click, "Grid coordinates: ", row, column)
        
        
    for grid in menu_grids:

        row,column=grid.evaluate_row_column_indices(click)
        
        index=grid.get_element_index(row,column)
        if index is not None:
            if grid==grids[1]:
                function_array=[set_value,set_value,set_value,set_value,set_value]
                parameter_array=[3,4,5,6,7]
            elif grid==grids[2]:
                function_array=[reset,nothing,nothing,add_inhabitant,nothing]
                parameter_array=[grids[0],grids[0],grids[0],0,20]
            function_array[index](parameter_array[index])

def nothing(x):
    pass

def reset(grid):
    terrains=[1]
    grid.generate_random_map(terrains)
    mem.food=50
    mem.gold=0
    mem.wood=0
    mem.inh=10
    mem.used_inh=0
    mem.value=3
    
def generate_terrain(grid):
    terrains=[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
    grid.generate_random_map(terrains)
    
def smooth_terrain(grid):
    grid.smooth_map(0)
    grid.smooth_map(2)
    
def add_inhabitant(value):
    if mem.food>=100:
        mem.inh+=1
        mem.food-=100
    
def set_value(value):
    mem.value=value
    
def turn(x):
    mem.gold=mem.gold+x
    
    

 
def check_resources(value):
    if value==3 and mem.wood>=200 and mem.inh-mem.used_inh>=5:
        return(True)
    elif value==4 and mem.wood>=500 and mem.inh-mem.used_inh>=5:
        return(True)
    elif value==5 and mem.wood>=1000 and mem.inh-mem.used_inh>=5:
        return(True)
    elif value==6 or value==7:
        return(True)
    
    else:
        return(False)

def pay_resources(value):
    if value==3:
        mem.wood-=200
        mem.used_inh+=5
    elif value==4:
        mem.wood-=500
        mem.used_inh+=5
    elif value==5:
        mem.wood-=1000
        mem.used_inh+=5

    
def set_element_value(grid,row,column,value,clicked=True):
    if not(column>=grid.columns or row>=grid.rows or column<0 or row<0):
        if grid.grid[row][column] not in [3,4,5,6,7]:
            enough_resources=check_resources(value)
            if enough_resources:
                pay_resources(value)
                grid.grid[row][column] = value
                if value==4:
                    mem.busy_buildings.append(0)
                if value==5:
                    mem.busy_farms.append(0)
        if grid.grid[row][column] in [6,7] and clicked:
            resource=grid.grid[row][column]
            grid.grid[row][column] = 1
            if resource==6:
                mem.food+=10
            if resource==7:
                mem.wood+=10
        

def count_objects(grid):
    """Count occurence of given items"""
    flat_grid=[]
    for i in range(0,grid.rows):
        flat_grid+=grid.grid[i]
    occurence=Counter(flat_grid)
    return(occurence)

def increment_resources(occurence):
    houses=occurence[3]
    woodcutters=occurence[4]
    farms=occurence[5]
    """increment"""
    mem.gold+=houses
    if mem.gold>=4*farms+2*woodcutters:
        mem.gold-=4*farms
        mem.gold-=2*woodcutters
        #mem.food+=farms
        #mem.wood+=woodcutters

   
def time_event(grids,time_fr):
    if time_fr%20==0:
        grid=grids[0]
        random_resource(grid)       
    if time_fr%60==0:
        if mem.food>0:
            mem.food-=mem.inh/60
            mem.inh=mem.inh*(1+0.1/60)
        if mem.food<=0:
            mem.food=0
            mem.inh=mem.inh*0.9
            
        occurence=count_objects(grid)
        increment_resources(occurence)
        
        buildings_pos=find_buildings(grid,4)
        near_distances,near_positions=find_nearest_resource(grid,7,buildings_pos)
        print(near_distances,near_positions,mem.busy_buildings)
        for i in range(len(mem.busy_buildings)):
            if mem.busy_buildings[i]==0:
                mem.busy_buildings[i]=5+math.floor(near_distances[i])
            elif mem.busy_buildings[i]==1:
                set_element_value(grid,near_positions[i].x,near_positions[i].y,1)
                mem.busy_buildings[i]-=1
            else:
                mem.busy_buildings[i]-=1
        print(mem.busy_buildings)
        
        
        
        buildings_pos=find_buildings(grid,5)
        near_distances,near_positions=find_nearest_resource(grid,6,buildings_pos)
        print(near_distances,near_positions,mem.busy_farms)
        for i in range(len(mem.busy_farms)):
            if mem.busy_farms[i]==0:
                mem.busy_farms[i]=5+math.floor(near_distances[i])
            elif mem.busy_farms[i]==1:
                set_element_value(grid,near_positions[i].x,near_positions[i].y,1)
                mem.busy_farms[i]-=1
            else:
                mem.busy_farms[i]-=1
        print(mem.busy_farms)
        
        
        
        
def find_buildings(grid,tile_value):
    buildings_pos=[]
    for row in range(grid.rows):
        for column in range(grid.columns):
            if grid.grid[row][column]==tile_value:
                buildings_pos.append(game_engine.Position([row,column]))
                
                
    return(buildings_pos)
    

def find_nearest_resource(grid,tile_value,positions):
    
    near_distances=list(range(100,100+len(positions)))
    near_positions=list(range(100,100+len(positions)))
    for row in range(grid.rows):
        for column in range(grid.columns):
            if grid.grid[row][column]==tile_value:
                pos=game_engine.Position([row,column])
                for i in range(len(positions)):
                    dist=pos.distance(positions[i])
                    if dist<near_distances[i]:
                        near_distances[i]=dist
                        near_positions[i]=pos
    return(near_distances,near_positions)
                    

    


def random_resource(grid):
    row=random.randint(0,grid.rows-1)
    column=random.randint(0,grid.columns-1)
    choice=random.choice([0,0,0,1])
    if choice==0:
        set_element_value(grid,row,column,7,clicked=False) 
    else:
        set_element_value(grid,row,column,6,clicked=False)
        
    

def update_labels(labels):
    labels[10].text="Gold: "+str(round(mem.gold))
    labels[11].text="Wood: "+str(round(mem.wood))
    labels[12].text="Food: "+str(round(mem.food))
    labels[13].text="Inhabitants: "+str(round(mem.inh-mem.used_inh))+"/"+str(round(mem.inh))
        #menu3=["Gold: "+str(mem.gold),"Wood: "+str(mem.wood), "Food: "+str(mem.food), "Inhabitants: "+str(mem.inhabitants)]    
    #for i in range(len(menu3)):    
     #   labels.append(game_engine.Label([1020,70+55*i],menu3[i],fontsize=20))