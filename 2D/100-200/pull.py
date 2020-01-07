#2017/08/06 LI Changsheng @nNanJing University
#change to real 2D 
#1.fix x and fix spin in y z
#2014-2015 Cai ShengYang @NanJing University

import math,sys,os
import numpy as np
from yade import pack, ymport

#basic parameters
case=0
v=0.1	

n_layer=10

def GenerateFold(path):

    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path)

#setting frict materials -----
fyoung = 9e10 #8e9
fpoisson = 0.25
frictAng = 0
fden = 2500

#setting rock materials -----
ryoung = 2e7 #2e7
rpoisson = 0.25
rfrictAng = math.atan(0.6)
rreps = 0.06
rden = 2500 #2500


#default:0-4 1-8e7
csnormalCohesion=2e7 #1
csshearCohesion=4e7 #2

frict = O.materials.append(FrictMat(young = fyoung,
                                poisson = fpoisson,
                                frictionAngle = frictAng,
                                density = fden))

#from xwq
rock = O.materials.append(CohFrictMat( young=ryoung,
                                            poisson=rpoisson,
                                            density=rden,
                                            frictionAngle=rfrictAng,
                                            normalCohesion=csnormalCohesion,
                                            shearCohesion=csshearCohesion,
                                            label='spheres'))


#adding deposit -----
sample = ymport.text('./sample.txt')
spheres = O.bodies.append(sample)

#building boxes -----
box_length = 200.0
box_height = 150.0
box_depth  = 10

#plus length after extension
box_length_plus=100

#wallMask
#determines which walls will be created, in the order
#-x(1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the
#default 63 means to create all walls
#parameter1:center
#parameter2:size
box = geom.facetBox(( box_length/2+box_length_plus, box_height/2,0),
                    ( box_length/2+box_length_plus, box_height/2,box_depth/2),
                    wallMask = 48,
                    material = frict)

#push plane
wall_right = utils.wall(box_length, axis = 0, material = frict)
wall_left = utils.wall(0, axis = 0, material = frict)

base = utils.wall(0, axis = 1, material = frict)

#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  

for i in spheres:
	#a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
	O.bodies[i].state.blockedDOFs='XYz'

#defining engines -----
savePeriod = int(2500/abs(v)) # save files for every iterPeriod steps
checkPeriod = int(savePeriod/5) #for print
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

maxl = max([O.bodies[i].state.pos[0] for i in spheres])
maxh = max([O.bodies[i].state.pos[1] for i in spheres])

#yade rgb list
yade_rgb_list=[ [0.50,0.50,0.50],
		[1.00,0.00,0.00],
		[0.00,1.00,0.00],
		[1.00,1.00,0.00],
		[0.85,0.85,0.85],
		[0.00,1.00,1.00],
		[1.00,0.00,1.00],
		[0.90,0.90,0.90],
		[0.15,0.15,0.15],
		[0.00,0.00,1.00] ]

rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[4:5]

#proper number of layer
while len(rgb_list)<n_layer:

	rgb_list*=2

rgb_detachment=yade_rgb_list[1]

#coloring the sample -----
height_step=maxh/(n_layer)

#thickness
height_base=case*height_step/2
height_salt=case*height_step/2
height_rock=maxh-height_base-height_salt

base_detachment=False
salt_detachment=False

#so many conditions
for i in spheres:

	#O.bodies[i].state.blockedDOFs='XYz'

	for k in range(n_layer):

		#rock
		if k*height_step<=O.bodies[i].state.pos[1]<=(k+1)*height_step:

			O.bodies[i].shape.color = rgb_list[k]
			O.bodies[i].material = O.materials[rock]

		#base detachment
		if base_detachment:

			if 0<=O.bodies[i].state.pos[1]<=height_base:

				O.bodies[i].shape.color = rgb_detachment
				O.bodies[i].material = O.materials[detachment]


		#salt detachment
		if salt_detachment:

			if maxh/2-height_salt/2<=O.bodies[i].state.pos[1]<=maxh/2+height_salt/2:
		
				O.bodies[i].shape.color = rgb_detachment
				O.bodies[i].material = O.materials[detachment]

	
print "The max height is %.3f" % maxh
print "The max length is %.3f" % maxl

#TW records stress data
TW=TesselationWrapper()
TW.computeVolumes()
stress=bodyStressTensors()

offset=wall_right.state.pos[0]-wall_left.state.pos[0]-box_length #wall ypos
progress=(offset/box_length)*100

folder_name='./extension/v=%.1f/input' %(abs(v))

if base_detachment:

	folder_name='./extension/base detachment/fric=%.1f v=%.1f/input/base=%.2f' %(dfric,abs(v),height_base)

if salt_detachment:

	folder_name='./extension/salt detachment/fric=%.1f v=%.1f/input/salt=%.2f' %(dfric,abs(v),height_base)


#Generate Fold
GenerateFold(folder_name)

out_file=open(folder_name+'/progress='+'%.2f%%' %progress+".txt",'w')

for b in sample:

    this_stress=stress[b.id]*4.*pi/3.*b.shape.radius**3/TW.volume(b.id)

    #print(this_stress)
    
    #id
    out_file.write(str(b.id))  
    out_file.write(',')

    #radius
    out_file.write(str(b.shape.radius))

    #color
    for this_color in b.shape.color:

        out_file.write(',')

        out_file.write(str(this_color))
    
    #position
    for this_pos in b.state.pos:

        out_file.write(',')

        out_file.write(str(this_pos))

    for this_line in this_stress:

	for this_str in this_line:

    	     out_file.write(',')
   	     out_file.write(str(this_str))

    out_file.write('\n')

#O.bodies.append(box)

O.bodies.append(wall_left)
O.bodies.append(wall_right)

O.bodies.append(base)

print 'case',case

O.run()

#pushing stage -----
def startPushing():
    
    if O.iter < pre_thres:
        return

    wall_left.state.vel = Vector3(-v, 0,0)
    wall_right.state.vel = Vector3( v, 0,0)
    base.state.vel = Vector3( 0, 0,0)

    controller.command = 'stopSimulation()'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder]
    

#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation():
    #global flag
    #global count
    
    print 'iter',O.iter
    
    offset=wall_right.state.pos[0]-wall_left.state.pos[0]-box_length #wall ypos

    #show where the wall is
    print 'the offset is %.2f' %offset 

    progress=(offset/box_length)*100

    #show the progress
    print 'the progress is %.2f%%' %progress
    
    print '\n'
    #save the state every 10% of the progress

    if O.iter%savePeriod==0:

	TW=TesselationWrapper()
	TW.computeVolumes()
	s=bodyStressTensors()

	out_file=open(folder_name+'/progress='+'%.2f%%' %progress+".txt",'w')

	for b in sample:

	    this_stress=s[b.id]*4.*pi/3.*b.shape.radius**3/TW.volume(b.id)

	    #print(this_stress)
	    
	    #id
	    out_file.write(str(b.id))
	    out_file.write(',')

	    #radius
	    out_file.write(str(b.shape.radius))

	    #color
	    for this_color in b.shape.color:

	        out_file.write(',')

	        out_file.write(str(this_color))
	    
	    #position
	    for this_pos in b.state.pos:

	        out_file.write(',')

	        out_file.write(str(this_pos))

	    for this_line in this_stress:

		for this_str in this_line:

	    	     out_file.write(',')
	   	     out_file.write(str(this_str))

	    out_file.write('\n')

    if progress/100 > 0.2:

	O.pause()    
 

