import os
import numpy as np
cwd = os.getcwd()

def processor(fend):
    "fend is file name to be processed"
    global list1
    end = open(fend,"r+")
    segment = 0
    list2 = [] #point positions
    list3 = [] #strain matrices
    list4 = [] #strain deviator
        
    for line in end:
        #marking the starts of each segments, segment 0 is put in list2, segment 2 is put in list3
        if "CELLS" in line:
            segment = 1
        if "POINT_DATA" in line:
            segment = 2
        if "SCALARS" in line:
            segment = 3
        
        if segment == 0:
            list2.append(line)
        elif segment == 2:
            list3.append(line)
        elif segment == 3:
            list4.append(line)
          
    end.close()
    
    entries = []
    EvList = ["SCALARS Volumetric_strain float 1", "LOOKUP_TABLE default"]
    EsList = ["SCALARS Shear_strain float 1", "LOOKUP_TABLE default"]
    
    for line in list3[2:-1]:
        if line != '\n':
            l = line.split()
            for i in range(len(l)):
                l[i] = float(l[i])
            entries.append(l)
    	
        else:
            DispGrad = np.mat(entries)
            StrainTensor = 0.5*(DispGrad + DispGrad.T)
            #print StrainTensor, '\n'
            Ev = np.trace(StrainTensor)
            EvList.append(Ev)
            Es = np.sqrt(StrainTensor[0,1]**2 + StrainTensor[0,2]**2 + StrainTensor[1,2]**2)
            EsList.append(Es)
            entries = []
        
    end = open(fend,"w")
    for line in list2 + list1 + list3 + list4:
        end.write(line)
        
    for i in EvList:
        end.write(str(i) + '\n')
    end.write('\n')
    for i in EsList:
        end.write(str(i) + '\n')
        
    end.close()

flist = []
for name in os.listdir(cwd):
    if ".vtk" in name:
        flist.append(name)
        
start = open("start.vtk", "r")

flag1 = 0
list1 = [] #use to store the original cell data
for line in start:
    if "CELLS" in line: #mark the beginning of cell data
        flag1 = 1
    if "POINT_DATA" in line: #quit as the cell data goes to end
        break
    if flag1:
        list1.append(line) #store cell data

for files in flist:
    processor(files)

