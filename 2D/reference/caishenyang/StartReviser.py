import os, math
cwd = os.getcwd()

def dist(a, b):
    """
    The dist function takes indexes of two points and returns the distance between them
    a: the first index
    b: the second index
    """
    p1 = points[a]
    p2 = points[b]
    d = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 +(p1[2]-p2[2])**2)
    return d        

def cell_judger(cell_vertex, d):
    """
    The cell_judger function takes the vertex information of a cell and judge whether it has an edge whose
    length exceeds the given value. If it does, returns True.
    cell_vertex: the vertex information of cells, also the elements in the cell list
    d: the greatest distrance allowed
    """
    for i in range(1,5):
        for j in range(i+1,5):
            if dist(cell_vertex[i],cell_vertex[j]) > d:
                return True
    
    return False

def f(which_vtk):
    
    start= open(which_vtk, "r")
    
    flag = 0
    header = []
    points = []
    cells = [] #use to store the original cell data
    cell_types = []
    point_data = []
    for line in start:
        if "POINTS" in line:
            header.append(line)
            flag = 1
            continue
        if "CELLS" in line: #mark the beginning of cell data
            flag = 2
            cell_info = line.split()
            cell_info = [cell_info[0]] + [int(i) for i in cell_info[1:]]
            cells.append(cell_info)
            continue
        if "CELL_TYPES" in line: #quit as the cell data goes to end
            flag = 3
        
        if "POINT_DATA" in line:
            flag = 4
        
        if flag == 0:
            header.append(line)
        
        if flag == 1:
            point_cord = line.split()
            point_cord = [float(i) for i in point_cord]
            if len(point_cord) != 0:
                points.append(point_cord)
        
        if flag == 2:
            cell_vertex = line.split()
            cell_vertex = [int(i) for i in cell_vertex]
            cells.append(cell_vertex)
                
        if flag == 4:
            point_data.append(line)
    
    
    for cell in cells[1:]:
        if cell_judger(cell, 20):
            cells.remove(cell)
            cells[0][1] -= 1
            cells[0][2] -= 5
    
    cell_num = cells[0][1] 
    
    cell_types = ["CELL_TYPES %d" % cell_num] + [10]*cell_num 
    
    start.close()
    
    start = open("start.vtk", "w")
    
    for line in header:
        start.write(line)
    for point in points:
        start.write(' '.join([str(i) for i in point]) + '\n')
    
    start.write('\n')
    
    for cell in cells:
        start.write(' '.join([str(i) for i in cell]) + '\n')
        
    for cell_type in cell_types:
        start.write(str(cell_type) + '\n')
    
    start.write('\n')
    
    for data in point_data:
        start.write(data)
    
    start.close()
      
#batch process
flist = []

for name in os.listdir(cwd):
    if ".vtk" in name:
        flist.append(name) 

for files in flist:
    f(files)
        
