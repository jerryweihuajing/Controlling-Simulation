#2017/08/06 LI Changsheng @nNanJing University
#change to real 2D 
#1.fix x and fix spin in y z
#2014-2015 Cai ShengYang @NanJing University

import math,sys,os
import numpy as np
from yade import pack, ymport

#basic parameters
case_base=1
case_salt=4

v= .4 #default 0.4
dfric=0.0 #default 0 
n_layer=10

direction='single'
exp_name=''

case_name=direction

erosion=False
deposit=False
swelling=False
fault=False
base_detachment=True
salt_detachment=True

deposit_thickness=10
deposit_distance=300
deposit_length=100
deposit_period=1

start_depth=50
end_depth=0
fault_distance=50
inclination=-30

salt_distance=0
salt_width=500

if fault:
    
    case_name+=' fault '+str(inclination)
    case_name+=' sD='+str(start_depth)
    case_name+=' eD='+str(end_depth)
    case_name+=' fD='+str(fault_distance)
    
if swelling:
    
    case_name+=' swelling'
    
if case_base>0:
    
    if base_detachment:
        
        case_name+=' base-'+str(case_base*5)+'km'

if case_salt>0:
    
    if salt_detachment:
        
        case_name+=' salt-'+str(case_salt*5)+'km'

        case_name+=' sD='+str(salt_distance)
        case_name+=' sW='+str(salt_width)
    
if exp_name!='':

    case_name+=(' '+exp_name)

if deposit:
    
    case_name+=' with deposit'
    
    case_name+=' dT='+str(deposit_thickness)
    case_name+=' dD='+str(deposit_distance)
    case_name+=' dL='+str(deposit_length)
    case_name+=' dP='+str(deposit_period)
    
if erosion:
    
    case_name+=' with erosion'
    
def GenerateFold(path):

    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path)

#setting frict materials -----
fyoung = 8e9
fpoisson = 0.25
frictAng = 0 #0
fden = 2500

#setting rock materials -----
ryoung = 2e7 #csy: 2e7 fyj: 2e8
rpoisson = 0.25
rfrictAng = math.atan(0.6) #csy: 0.6 fyj: 0.3
rreps = 0.06
rden = 2500 #2500

#setting detachment materials ----- 
dyoung = 2e8 #csy: 2e7 fyj: 2e8
dpoisson = 0
dfrictAng = math.atan(dfric) 
dreps = 0.001
dden = 2100 #csy: 2100 fyj:2300

m_wall = O.materials.append(FrictMat(young = fyoung,
                                     poisson = fpoisson,
                                     frictionAngle = frictAng,
                                     density = fden))
                                                                       
m_rock = O.materials.append(CpmMat(young = ryoung,
                                   poisson = rpoisson,
                                   frictionAngle = rfrictAng,
                                   epsCrackOnset = rreps,
                                   density = rden,
                                   relDuctility = 0))

m_detachment = O.materials.append(CpmMat(young = dyoung,
                                         poisson = dpoisson,
                                         frictionAngle = dfrictAng,
                                         epsCrackOnset = dreps,
                                         density = dden,
                                         relDuctility = 0))

#swelling
m_swelling = O.materials.append(CpmMat(young = 100*ryoung,
                                       poisson = rpoisson,
                                       frictionAngle = rfrictAng,
                                       epsCrackOnset = rreps,
                                       density = rden,
                                       relDuctility = 0))

#building boxes -----
box_length = 500.0
box_height = 100.0
box_depth  = 5

#wallMask
#determines which walls will be created, in the order
#-x(1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the
#default 63 means to create all walls
#parameter1:center
#parameter2:size
box = geom.facetBox(( box_length/2, box_height/2,0),
                    ( box_length/2, box_height/2,box_depth/2),
                    wallMask = 0,
                    material = m_wall)

#push plane
wall_right = utils.wall(box_length, axis = 0, material = m_wall)
wall_left = utils.wall(0, axis = 0, material = m_wall)
wall_bottom= utils.wall(0, axis = 1, material = m_wall)

O.bodies.append(wall_right)
O.bodies.append(wall_left)
O.bodies.append(wall_bottom)

#adding deposit -----
spheres = ymport.text('./sample.txt')
id_spheres = O.bodies.append(spheres)

#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  
for i in id_spheres:
	#a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
	O.bodies[i].state.blockedDOFs='XYz'

maxl = max([O.bodies[i].state.pos[0] for i in id_spheres])
maxh = max([O.bodies[i].state.pos[1] for i in id_spheres])

#defining engines -----
savePeriod = int(8000/abs(v)) # save files for every iterPeriod steps
checkPeriod = savePeriod/100 #int(savePeriod/5) #for print
pre_thres = checkPeriod  #for deposition which is not already done

O.engines = [	
ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor = 1, label = 'ctr1'), Bo1_Facet_Aabb(), Bo1_Wall_Aabb()], verletDist = 0.1),
InteractionLoop(
    [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor = 1, label = 'ctr2'), Ig2_Facet_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
    [Ip2_CpmMat_CpmMat_CpmPhys(cohesiveThresholdIter = pre_thres), Ip2_FrictMat_CpmMat_FrictPhys(), Ip2_FrictMat_FrictMat_FrictPhys()],
    [Law2_ScGeom_FrictPhys_CundallStrack(), Law2_ScGeom_CpmPhys_Cpm()],
    ),

NewtonIntegrator(damping = 0.4, gravity = (0,-9.81,0)),
PyRunner(command = 'startPushing()', iterPeriod = checkPeriod, label = 'controller'),
]

#snapshot = qt.SnapshotEngine(fileBase='-',iterPeriod=savePeriod)
#vtkRecorder = VTKRecorder(fileName='0.00%-',recorders=['all'],iterPeriod=savePeriod)

O.dt =3* utils.PWaveTimeStep()
#O.dt=0.0027

TW1 = TesselationWrapper() #TW1 records cumulative strain data
TW1.setState(0)
TW1.setState(1)
#TW1.defToVtk("./cumulative strain/start.vtk")

TW2 = TesselationWrapper() #TW2 records periodical strain data
TW2.setState(0)

#yade rgb list
yade_rgb_list=[[0.50,0.50,0.50],
               [1.00,0.00,0.00],
               [0.00,1.00,0.00],
               [1.00,1.00,0.00],
               [0.85,0.85,0.85],
               [0.00,1.00,1.00],
               [1.00,0.00,1.00],
               [0.90,0.90,0.90],
               [0.15,0.15,0.15],
               [0.00,0.00,1.00]]

#grey: yade_rgb_list[4:5]
#black: yade_rgb_list[-2:-1]
#green: yade_rgb_list[2:3]
#yellow: yade_rgb_list[3:4]

base_rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[4:5]
lower_base_rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[5:6]
upper_base_rgb_list=yade_rgb_list[6:7]+yade_rgb_list[4:5]
deposit_rgb_list=yade_rgb_list[2:4]+yade_rgb_list[9:]+yade_rgb_list[0:1]+yade_rgb_list[5:7]

#proper number of layer
while len(base_rgb_list)<n_layer:

	base_rgb_list*=2
    
#proper number of layer
while len(upper_base_rgb_list)<n_layer:

	upper_base_rgb_list*=2

#proper number of layer
while len(lower_base_rgb_list)<n_layer:

	lower_base_rgb_list*=2
        
while len(deposit_rgb_list)<20:

	deposit_rgb_list*=2
    
rgb_swelling=yade_rgb_list[-1]
rgb_detachment=yade_rgb_list[1]
rgb_green=yade_rgb_list[2]
rgb_yellow=yade_rgb_list[3]
#coloring the sample -----
height_step=maxh/(n_layer)

#thickness
height_base=case_base*height_step/2
height_salt=case_salt*height_step/2
height_rock=maxh-height_base-height_salt

#define swelling
swelling_height=maxh*0.3
swelling_length=maxl*0.7

k_swelling=swelling_height/swelling_length

map_height_swelling={}

for k in range(int(box_length)):
    
    if k<swelling_length and swelling:
        
        map_height_swelling[k]=swelling_height-k_swelling*k
    
    else:
        
        map_height_swelling[k]=0
        
#map between y and x tuple
map_fault_y_x={}

k=np.tan(inclination*np.pi/180)

if k>0:
    
    b=start_depth-k*(maxl-fault_distance)
    
if k<0:
    
    b=end_depth-k*(maxl-fault_distance)
    
fault_width=np.abs(3/np.sin(inclination*np.pi/180))

for this_y in range(end_depth,start_depth):
    
    this_x=(this_y-b)/k
    
    map_fault_y_x[int(this_y)]=(this_x-fault_width/2,this_x+fault_width/2)

#so many conditions
for i in id_spheres:

	#O.bodies[i].state.blockedDOFs='XYz'

    for k in range(n_layer):

        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
        
        if k*height_step<=this_y<=(k+1)*height_step:
            
            O.bodies[i].shape.color = base_rgb_list[k]
            O.bodies[i].material = O.materials[m_rock]
                
            #salt detachment
            if salt_detachment:
                
                y_min=maxh/2
                y_max=maxh/2+height_salt
                x_min=maxl-salt_distance-salt_width
                x_max=maxl-salt_distance
                
                if y_min<=this_y<=y_max and x_min<=this_x<=x_max:
    		
                    O.bodies[i].shape.color = rgb_detachment
                    O.bodies[i].material = O.materials[m_detachment]
 
            #swelling
            if swelling:
                
                y_min=0
                y_max=map_height_swelling[int(this_x)]
                
                if y_min<=this_y<=y_max:
                    
                    O.bodies[i].shape.color = rgb_swelling
                    O.bodies[i].material = O.materials[m_swelling]

                    O.bodies[i].state.blockedDOFs='xyz'
                    
            #base detachment
            if base_detachment:
    
                y_min=map_height_swelling[int(this_x)]
                y_max=map_height_swelling[int(this_x)]+height_base
                
                if y_min<=this_y<=y_max:
                    
                    O.bodies[i].shape.color = rgb_detachment
                    O.bodies[i].material = O.materials[m_detachment]  
                    
            if fault:
                
                if int(this_y) in list(map_fault_y_x.keys()):
                    
                    x_min=map_fault_y_x[int(this_y)][0]
                    x_max=map_fault_y_x[int(this_y)][1]
                        
                    if x_min<=this_x<=x_max:
      
                        O.bodies[i].shape.color = rgb_detachment
                        O.bodies[i].material = O.materials[m_detachment]  
                
print "The max height is %.3f" % maxh
print "The max length is %.3f" % maxl

#TW records stress data
TW=TesselationWrapper()
TW.computeVolumes()
stress=bodyStressTensors()

offset=box_length-(wall_right.state.pos[0]-wall_left.state.pos[0]) #wall ypos
progress=(offset/box_length)*100

folder_name='./input//'+case_name

#Generate Fold
GenerateFold(folder_name)

out_file=open(folder_name+'/A_progress='+'%.2f%%' %progress+".txt",'w')
 
def Erosion(which_O,y_max):
    
    old_bodies=[1 for this_body in which_O.bodies if this_body!=None]
    
    spheres=[]  
    
    #create idx list for deleting
    idx_to_delete=[]
    
    for k in range(3,len(which_O.bodies)):

        if which_O.bodies[k]==None:
            
            continue
        
        if which_O.bodies[k].state.pos[1]>y_max:
        
            idx_to_delete.append(k)
            
        else:
            
            spheres.append(O.bodies[k])
            
    print ''
    print 'before delete'
    print 'amount of bodies:',len(old_bodies)   
    
    #delete from O.bodies
    for this_idx in idx_to_delete:
        
        which_O.bodies.erase(this_idx)
        
    new_bodies=[1 for this_body in which_O.bodies if this_body!=None]
    
    print ''
    print 'after delete'
    print 'amount of bodies:',len(new_bodies)
    print 'amount of spheres:',len(spheres)
    
    return spheres

def RecordData(out_file,which_spheres):
    
    print ''
    print 'Record Data'
    print 'amount of spheres:',len(which_spheres)
    
	#TW records stress data
    TW=TesselationWrapper()
    TW.computeVolumes()
    stress=bodyStressTensors()

    for this_sphere in which_spheres:

        this_stress=stress[this_sphere.id]*4.*pi/3.*this_sphere.shape.radius**3/TW.volume(this_sphere.id)

	    #print(this_stress)
	    
	    #id
        out_file.write(str(this_sphere.id))  
        out_file.write(',')

	    #radius
        out_file.write(str(this_sphere.shape.radius))

	    #color
        for this_color in this_sphere.shape.color:

            out_file.write(',')
            out_file.write(str(this_color))
	    
	    #position
        for this_pos in this_sphere.state.pos:

            out_file.write(',')
            out_file.write(str(this_pos))

        #velocity
        for this_vel in this_sphere.state.vel:

            out_file.write(',')
            out_file.write(str(this_vel))
        
        #stress
        for this_line in this_stress:
            
            for this_str in this_line:
                
                out_file.write(',')
                out_file.write(str(this_str))

        out_file.write('\n')

RecordData(out_file,spheres)

O.run()

print ''
print '-- Simulation on'
print '-> case:',case_name
print ''

#pushing stage -----
def startPushing():
    
    if O.iter < pre_thres:
        
        return

    if direction=='double':

        wall_left.state.vel = Vector3( v/2, 0,0)
        wall_right.state.vel = Vector3( -v/2, 0,0)
        wall_bottom.state.vel = Vector3( 0, 0,0)

    if direction=='single-2':

        wall_left.state.vel = Vector3( 0, 0,0)
        wall_right.state.vel = Vector3( -v, 0,0)
        wall_bottom.state.vel = Vector3( -v, 0,0)

    if direction=='single':

        wall_left.state.vel = Vector3( 0, 0,0)
        wall_right.state.vel = Vector3( -v, 0,0)
        wall_bottom.state.vel = Vector3( 0, 0,0)
        
    controller.command = 'stopSimulation(deposit,\
                            erosion,\
                            deposit_thickness,\
                            deposit_length,\
                            deposit_distance,\
                            deposit_period)'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder] 

#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation(deposit,
                   erosion,
                   deposit_thickness,
                   deposit_length,
                   deposit_distance,
                   deposit_period):
    
    offset=box_length-(wall_right.state.pos[0]-wall_left.state.pos[0]) #wall ypos
    progress=(offset/box_length)*100

    print 'iter',O.iter
    print 'the offset is %.2f' %offset 
    print 'the progress is %.2f%%' %progress
    print ''

    if O.iter%savePeriod==0:
        
        out_file=open(folder_name+'/A_progress=%.2f%%' %progress+".txt",'w')
        
        #make erosion
        if erosion:
  
            erosion_height=0.9*max([O.bodies[k].state.pos[1] for k in range(3,len(O.bodies)) if O.bodies[k]!=None])
                
            spheres=Erosion(O,erosion_height)
            
        else:
            
            spheres=[O.bodies[k] for k in range(3,len(O.bodies))]
            
        RecordData(out_file,spheres)
        
    if O.iter%savePeriod==3*checkPeriod:
        
        #flag to deposit
        flag_deposit=True
        
        out_file=open(folder_name+'/B_progress=%.2f%%' %progress+".txt",'w')
    
        #make erosion
        if erosion:
  
            erosion_height=0.9*max([O.bodies[k].state.pos[1] for k in range(3,len(O.bodies)) if O.bodies[k]!=None])
                
            spheres=Erosion(O,erosion_height)
            
        else:
            
            spheres=[O.bodies[k] for k in range(3,len(O.bodies))]
        
        RecordData(out_file,spheres)
        
        #end the loop
        if O.iter==7*savePeriod+3*checkPeriod:

            O.pause()
            
            print ''
            print '-- Simulation off'
            
        #make deposition 
        if O.iter>savePeriod and deposit and (O.iter==deposit_period*savePeriod+3*checkPeriod): #front mountain
        
            #save the state every 10% of the progress
            x_max = max([this_sphere.state.pos[0] for this_sphere in spheres])
            y_max = max([this_sphere.state.pos[1] for this_sphere in spheres])
            x_min = min([this_sphere.state.pos[0] for this_sphere in spheres])
            y_min = min([this_sphere.state.pos[1] for this_sphere in spheres])
                    
        	#adding deposit -----
            deposit_pack = pack.SpherePack()
            deposit_pack.makeCloud((x_max-deposit_distance-deposit_length, y_max, 0.0),
                                   (x_max-deposit_distance, y_max+2*deposit_thickness,0),
                                   rMean = 1, rRelFuzz = 0.2)
            deposit_pack.toSimulation(material = m_rock)
    
            print 'amount of deposit',len(deposit_pack)
        
            spheres_deposit=[O.bodies[idx] for idx in range(len(O.bodies)-len(deposit_pack),len(O.bodies))]
                
            for this_sphere in spheres_deposit:
                
                this_sphere.shape.color=rgb_green
 
