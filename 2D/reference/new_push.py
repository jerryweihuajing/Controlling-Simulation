import math,sys
sys.path.append('./')
import get_color_map as Color
from yade import qt, pack, ymport
from tool import GenerateFold

#setting frict materials -----
fyoung = 8e9
fpoisson = 0.25
ffrictAng = math.atan(0.6)
fden = 2500

#setting rock materials -----
ryoung = 2e7
rpoisson = 0.25
rfrictAng = math.atan(0.6)
rreps = 0.06
rden = 2500

#setting detachment materials ----- 
dyoung = 2e7
dpoisson = 0
dfrictAng = math.atan(0)
dreps = 0.001
dden = 2100

velocity=1 #wall push velocity
savePeriod = int(5000/velocity)
pyRunnerPeriod = 1000
crackRecordPeriod = 2000

n_layer=8
case=4

#geometric parameters-----
box_length = 2000.0
box_height = 100.0
box_depth  = 5.0
box_size=(box_length,box_height,box_depth)
TENSILESTRENGTH = 4.5e6
COHESION = 5e6
baseFrictAng = 0.5
wallFrictAng = 18
Enlarge = 1.01
OUT = 'T%.1f_C%.1f_BA%.1f_WA%.1f_ENLARGE%.2f0%%' % (TENSILESTRENGTH/1e6,COHESION/1e6,rfrictAng,ffrictAng,Enlarge)

#wall parameters -----
frict_material = O.materials.append(JCFpmMat(
	type = 0,
    young = fyoung,
    poisson = fpoisson,
    frictionAngle = ffrictAng,
    ))

#particle parameters -----
rock_material = O.materials.append(JCFpmMat(
    young = ryoung,
    poisson = rpoisson,
    frictionAngle = rfrictAng,
    density = rden,
    tensileStrength = TENSILESTRENGTH,
	cohesion = COHESION,
	))

#detachment parameters -----
detachment_material = O.materials.append(JCFpmMat(
    young = dyoung,
    poisson = dpoisson,
    frictionAngle = dfrictAng,
    density = dden,
    tensileStrength = TENSILESTRENGTH,
	cohesion = COHESION,
	))

#engines -----
O.engines = [
    ForceResetter(),
    InsertionSortCollider([Bo1_Box_Aabb(),Bo1_Facet_Aabb(),Bo1_Sphere_Aabb(aabbEnlargeFactor=Enlarge,label='EF')]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=Enlarge,label='DF'),Ig2_Box_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
		[Ip2_JCFpmMat_JCFpmMat_JCFpmPhys(cohesiveTresholdIteration=1,label='interactionPhys')],
		[Law2_ScGeom_JCFpmPhys_JointedCohesiveFrictionalPM(recordCracks=False,Key=OUT,label='interactionLaw')]
	),
    GlobalStiffnessTimeStepper(active=1, timeStepUpdateInterval=100, timestepSafetyCoefficient=0.5),
    NewtonIntegrator(damping = 0.4, gravity = (0,0,-9.81)),
    PyRunner(command = 'Coloring()', iterPeriod = pyRunnerPeriod, label = 'ctr'),   
    ]
#PyRunner(command = 'crackRecorder()',iterPeriod = crackRecordPeriod, label = 'crkRec') 
  
snapShot = qt.SnapshotEngine(fileBase='',initRun = True, iterPeriod=savePeriod)
vtkRecord = VTKRecorder(fileName='',initRun = True,recorders=['spheres','intr','colors','velocity','stress','jcfpm','cracks'],Key = OUT, iterPeriod=savePeriod)


sample = ymport.text('sample.txt')
spheres = O.bodies.append(sample)
    
for i in spheres:

	O.bodies[i].material = O.materials[rock_material]

GenerateFold('./cumulative strain')
GenerateFold('./periodical strain')
GenerateFold('./stress')
  
TW1 = TesselationWrapper() #TW1 records cumulative strain data
TW1.setState(0)
TW1.setState(1)
#TW1.defToVtk("start.vtk")

TW2 = TesselationWrapper() #TW2 records periodical strain data
TW2.setState(0)

 
#walls must be constructed after tesselation wrapper
box = utils.aabbWalls([(0,0,0),box_size], thickness = 3)
O.bodies.append(box)

#attribute
for this_wall in box:

	this_wall.material = O.materials[frict_material]

O.bodies.erase(box[5].id)
 
wall = box[0]
wall.material = O.materials[frict_material]
    
#==============================================================================        
def Coloring():
    
	EF.aabbEnlargeFactor = 1
	DF.interactionDetectionFactor = 1
    
	yade_rgb_list=Color.get_color_map('ColorRicebal.txt')[0]

	maxh = max([O.bodies[i].state.pos[1] for i in spheres])
	maxl = max([O.bodies[i].state.pos[0] for i in spheres])
	
	#coloring the sample -----
	height_step=maxh/n_layer
	
	for i in spheres:

		for k in range(n_layer):

			#case0
			if k*height_step<=O.bodies[i].state.pos[1]<=(k+1)*height_step:

				O.bodies[i].shape.color = yade_rgb_list[k]
				O.bodies[i].material = O.materials[rock_material]

				#case1
				if case==1:
					if k==4:

						O.bodies[i].shape.color = yade_rgb_list[4]
						O.bodies[i].material = O.materials[detachment_material]

				#case2
				if case==2:
					if k==4 or k==3:

						O.bodies[i].shape.color = yade_rgb_list[4]
						O.bodies[i].material = O.materials[detachment_material]

				#case3
				if case==3:
					if k==4 or k==3 or k==5:

						O.bodies[i].shape.color = yade_rgb_list[4]
						O.bodies[i].material = O.materials[detachment_material]

				#case4
				if case==4:
					if k==4 or k==3 or k==5 or k==2:
							
						O.bodies[i].shape.color = yade_rgb_list[4]
						O.bodies[i].material = O.materials[detachment_material]
                        
	print "The max length is %.3f" % maxl
	ctr.command = 'Push()'

#==============================================================================
def Push():
        
	offset=wall.state.pos[0] #wall ypos
	progress=(offset/box_length)*100
	file_name = str(progress)+'='+'%.2f%%' %progress
	snapShot.fileBase = vtkRecord.fileName = file_name
	O.engines = O.engines
	wall.state.vel = (velocity, 0, 0)
	ctr.command = 'Stop()'

#==============================================================================
def Stop():
	
	offset=wall.state.pos[0] #wall ypos
	progress=(offset/box_length)*100

	print ''
	print 'iter',O.iter #show where the iter	
	print 'the offset is %.2f' %offset #show where the wall is	
	print 'the progress is %.2f%%' %progress #show the progress

	file_name = str(progress)+'='+'%.2f%%' %progress
	snapShot.fileBase = vtkRecord.fileName = file_name
    
	if (O.iter-pyRunnerPeriod)%savePeriod == 0:
        
		RecordStrain()
		RecordStress()
        
	if offset > box_length*0.5:
        
		O.pause()
 
#==============================================================================       
def RecordStress():

	#TW records stress data
	TW=TesselationWrapper()
	TW.computeVolumes()
	stress=bodyStressTensors()

	offset=wall.state.pos[0] #wall ypos
	progress=(offset/box_length)*100

	out_file=open('./stress/stress'+'%.2f%%' %progress+".txt",'w')

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

#==============================================================================
def RecordStrain():

	offset=box_length-wall.state.pos[0] #wall ypos
	progress=(offset/box_length)*100
	
	#TW1 records cumulative strain data
	TW1.setState(1)
	TW1.defToVtk("./cumulative strain/progress="+'%.2f%%' %progress+".vtk")

	#TW2 records periodical strain data
	TW2.setState(1)
	TW2.defToVtk("./periodical strain/progress="+'%.2f%%' %progress+".vtk")

	TW2.setState(0)

    
