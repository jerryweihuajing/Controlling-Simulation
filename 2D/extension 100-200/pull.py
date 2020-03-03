#2017/08/06 LI Changsheng @nNanJing University
#change to real 2D 
#1.fix x and fix spin in y z
#2014-2015 Cai ShengYang @NanJing University

import math,sys,os
import copy as cp
import numpy as np
from yade import pack, ymport

#basic parameters
v=.2 #0.2
n_layer=10

direction='single-2'

case_name=''
case_name+=direction

swelling=False
detachment=False

if swelling:
    
    case_name+=' swelling'
    
def GenerateFold(path):

    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path)

#setting frict materials -----
fyoung = 8e9 #8e9
fpoisson = 0.25
frictAng = 0
fden = 2500

#setting rock materials -----
ryoung = 2e7 #csy: 2e7 fyj: 2e8
rpoisson = 0.25
rfrictAng = math.atan(0.6) #csy: 0.6 fyj: 0.3
rreps = 0.06
rden = 2500 #2500

#default:0-4 1-8e7
csnormalCohesion=2e7 #2
csshearCohesion=4e7 #4

#wall
m_wall = O.materials.append(FrictMat(young = fyoung,
                                     poisson = fpoisson,
                                     frictionAngle = frictAng,
                                     density = fden))

#base and deposit
m_rock = O.materials.append(CohFrictMat(young=ryoung,
                                        poisson=rpoisson,
                                        density=rden,
                                        frictionAngle=rfrictAng,
                                        normalCohesion=csnormalCohesion,
                                        shearCohesion=csshearCohesion,
                                        label='rock'))

m_detachment = O.materials.append(CohFrictMat(young=ryoung,
                                              poisson=rpoisson,
                                              density=rden,
                                              frictionAngle=0,
                                              normalCohesion=csnormalCohesion,
                                              shearCohesion=csshearCohesion,
                                              label='detachment'))
#swelling
m_swelling = O.materials.append(CohFrictMat(young=ryoung,
                                            poisson=rpoisson,
                                            density=rden,
                                            frictionAngle=rfrictAng,
                                            normalCohesion=csnormalCohesion*100,
                                            shearCohesion=csshearCohesion*100,
                                            label='swelling'))

#building boxes -----
box_length = 200.0
box_height = 100.0
box_depth  = 10

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
wall_bottom = utils.wall(0, axis = 1, material = m_wall)

O.bodies.append(wall_left)
O.bodies.append(wall_right)
O.bodies.append(wall_bottom)

#adding deposit -----
#spheres = ymport.text('./standard sample.txt')
spheres = ymport.text('./sample.txt')

#list object
id_spheres = O.bodies.append(spheres)

#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  

for i in id_spheres:

	#a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
	O.bodies[i].state.blockedDOFs='XYz'

#defining engines -----
savePeriod = int(2400/abs(v)) # save files for every iterPeriod steps
checkPeriod = int(savePeriod/100) #for print
pre_thres = checkPeriod #for deposition which is not already done

O.engines = [	
ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor = 1, label = 'ctr1'), Bo1_Facet_Aabb(), Bo1_Wall_Aabb()], verletDist = 0.1),
InteractionLoop(
    [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor = 1, label = 'ctr2'), Ig2_Facet_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
    [Ip2_CpmMat_CpmMat_CpmPhys(cohesiveThresholdIter = pre_thres), Ip2_FrictMat_CpmMat_FrictPhys(), Ip2_FrictMat_FrictMat_FrictPhys()],
    [Law2_ScGeom_FrictPhys_CundallStrack(), Law2_ScGeom_CpmPhys_Cpm()],
    ),

NewtonIntegrator(damping = 0.4, gravity = (0,-9.81,0)),
PyRunner(command = 'startPushing()', iterPeriod = checkPeriod, label = 'controller'),]

#snapshot = qt.SnapshotEngine(fileBase='-',iterPeriod=savePeriod)
#vtkRecorder = VTKRecorder(fileName='0.00%-',recorders=['all'],iterPeriod=savePeriod)

O.dt =1* utils.PWaveTimeStep()

TW1 = TesselationWrapper() #TW1 records cumulative strain data
TW1.setState(0)
TW1.setState(1)
#TW1.defToVtk("./cumulative strain/start.vtk")

TW2 = TesselationWrapper() #TW2 records periodical strain data
TW2.setState(0)

maxl = max([O.bodies[i].state.pos[0] for i in id_spheres])
maxh = max([O.bodies[i].state.pos[1] for i in id_spheres])

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

base_rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[4:5]
deposit_rgb_list=yade_rgb_list[2:4]+yade_rgb_list[9:]+yade_rgb_list[0:1]+yade_rgb_list[5:7]

#proper number of layer
while len(base_rgb_list)<n_layer:

	base_rgb_list*=2

while len(deposit_rgb_list)<20:

	deposit_rgb_list*=2

rgb_swelling=yade_rgb_list[0]
rgb_detachment=yade_rgb_list[1]

#coloring the sample -----
height_step=maxh/(n_layer)

#so many conditions
for i in id_spheres:

	#O.bodies[i].state.blockedDOFs='XYz'

    for k in range(n_layer):

		#rock
        if k*height_step<=O.bodies[i].state.pos[1]<=(k+1)*height_step:
            
            O.bodies[i].shape.color = base_rgb_list[k]
            O.bodies[i].material = O.materials[m_rock]
            
    #swelling
    if swelling:

        if box_length*0.4<=O.bodies[i].state.pos[0]<=box_length*0.6:
            
            O.bodies[i].shape.color = rgb_swelling
            O.bodies[i].material = O.materials[m_swelling]
        
    if detachment:
        
        #base detachment
        if  O.bodies[i].state.pos[1]<=height_step/5:
            
            O.bodies[i].shape.color = rgb_detachment
            O.bodies[i].material = O.materials[m_detachment]
        
print "The max height is %.3f" % maxh
print "The max length is %.3f" % maxl

#TW records stress data
TW=TesselationWrapper()
TW.computeVolumes()
stress=bodyStressTensors()

offset=wall_right.state.pos[0]-wall_left.state.pos[0]-box_length #wall ypos
progress=(offset/box_length)*100

folder_name='./input//'+case_name

#Generate Fold
GenerateFold(folder_name)

out_file=open(folder_name+'/A_progress='+'%.2f%%' %progress+".txt",'w')

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

spheres_base=spheres

O.run()

print ''
print '-- Simulation on'
print '-> case:',case_name
print ''

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
    
#pushing stage -----
def startPushing():
    
    if O.iter < pre_thres:
        return

    if direction=='double-1':

        wall_left.state.vel = Vector3(-v/2, 0,0)
        wall_right.state.vel = Vector3( v/2, 0,0)
    
    if direction=='double-2':

        wall_left.state.vel = Vector3(-v/2, 0,0)
        wall_right.state.vel = Vector3( v/2, 0,0)
        wall_bottom.state.vel = Vector3( v/2, 0,0)
        
    if direction=='double diff-1':

        wall_left.state.vel = Vector3( -v/4, 0,0)
        wall_right.state.vel = Vector3( 3*v/4, 0,0)
        wall_bottom.state.vel = Vector3( 3*v/4, 0,0)
        
    if direction=='double diff-2':

        wall_left.state.vel = Vector3( -v/4, 0,0)
        wall_right.state.vel = Vector3( 3*v/4, 0,0)  
        wall_bottom.state.vel = Vector3( -v/4, 0,0)
        
    if direction=='single-1':

        wall_right.state.vel = Vector3( v, 0,0)
      
    if direction=='single-2':

        wall_right.state.vel = Vector3( v, 0,0)
        wall_bottom.state.vel = Vector3( v, 0,0)
        
    controller.command = 'stopSimulation(spheres_base)'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder]

#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation(spheres_base):
    
    offset=wall_right.state.pos[0]-wall_left.state.pos[0]-box_length #wall ypos
    progress=(offset/box_length)*100

    print 'iter',O.iter
    print 'the offset is %.2f' %offset 
    print 'the progress is %.2f%%' %progress
    print ''
     
    '''A'''
    if O.iter%savePeriod==0:
        
        out_file=open(folder_name+'/A_progress=%.2f%%' %progress+".txt",'w')
        
        spheres=[O.bodies[k] for k in range(3,len(O.bodies))]
            
        RecordData(out_file,spheres)
        
    '''B'''
    if O.iter%savePeriod==3*checkPeriod:
        
        #flag to deposit
        flag_deposit=True
        
        out_file=open(folder_name+'/B_progress='+'%.2f%%' %progress+".txt",'w')
        
        y_max_base=max([this_sphere.state.pos[1] for this_sphere in spheres_base])
    
        print 'max height of base is %.2f'%y_max_base
    
        spheres=Erosion(O,y_max_base)
        
        RecordData(out_file,spheres)
        
        #end the loop
        if O.iter==7*savePeriod+3*checkPeriod:

            O.pause()
            
            print ''
            print '-- Simulation off'

            flag_deposit=False
            
        #make deposition
        if O.iter>savePeriod and flag_deposit:
            
            #save the state every 10% of the progress
            x_max = max([this_sphere.state.pos[0] for this_sphere in spheres])
            y_max = max([this_sphere.state.pos[1] for this_sphere in spheres])
            x_min = min([this_sphere.state.pos[0] for this_sphere in spheres])
            y_min = min([this_sphere.state.pos[1] for this_sphere in spheres])
                    
        	#adding deposit -----
            deposit_thickness = 2*height_step #not the final thickness 
            deposit_cellpadding=0*(x_max-x_min)/10
            deposit = pack.SpherePack()
            deposit.makeCloud((x_min+deposit_cellpadding, y_max, 0.0),
                              (x_max-deposit_cellpadding, y_max+deposit_thickness,0),
                              rMean = 0.6, rRelFuzz = 0.12)
            deposit.toSimulation(material = m_rock)
    
            print 'amount of deposit',len(deposit)
        
            spheres_deposit=[O.bodies[idx] for idx in range(len(O.bodies)-len(deposit),len(O.bodies))]
    	
            color_idx=O.iter//savePeriod-1
    
            for this_sphere in spheres_deposit:
                
                this_sphere.shape.color=deposit_rgb_list[color_idx]
