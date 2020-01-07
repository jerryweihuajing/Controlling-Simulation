from yade import pack, qt, ymport
import math,sys

savePeriod = 40000
pyRunnerPeriod = 2000
crackRecordPeriod = 2000

#geometric parameters-----
l = 600 #box length
d = 4 #box depth
h = 200 #box height
TENSILESTRENGTH = 4.5e6
COHESION = 5e6
baseFrictAng = 0.5
wallFrictAng = 18
Enlarge = 1.01
OUT = 'T%.1f_C%.1f_BA%.1f_WA%.1f_ENLARGE%.2f0%%' % (TENSILESTRENGTH/1e6,COHESION/1e6,baseFrictAng,wallFrictAng,Enlarge)

wall_mat = O.materials.append(JCFpmMat(
	type = 0,
    young = 5e13,
    poisson = 1,
    frictionAngle = math.radians(baseFrictAng),
    ))

w_left_mat = O.materials.append(JCFpmMat(
	type = 0,
    young = 5e13,
    poisson = 1,
    frictionAngle = math.radians(wallFrictAng),
    ))

#particle parameters -----
    
sphere_mat = O.materials.append(JCFpmMat(
    young = 5e9,
    poisson = 1.0/3,
    frictionAngle = math.radians(18),
    density = 4800,
    tensileStrength = TENSILESTRENGTH,
	cohesion = COHESION,
	))


s = ymport.text('dens2691Young5.0GPaL600H45.txt')
spheres = O.bodies.append(s)

for i in spheres:
	O.bodies[i].material = O.materials[sphere_mat]


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
    PyRunner(command = 'coloring()', iterPeriod = pyRunnerPeriod, label = 'ctr'),
    PyRunner(command = 'crackRecorder()',iterPeriod = crackRecordPeriod, label = 'crkRec')
    ]
    
snapShot = qt.SnapshotEngine(fileBase='',initRun = True, iterPeriod=savePeriod)
vtkRecord = VTKRecorder(fileName='',initRun = True,recorders=['spheres','intr','colors','velocity','stress','jcfpm','cracks'],Key = OUT, iterPeriod=savePeriod)

TW1 = TesselationWrapper() #TW1 records cumulative strain data
TW1.setState(0)
TW1.setState(1)
TW1.defToVtk("start.vtk")

TW2 = TesselationWrapper() #TW2 records periodical strain data
TW2.setState(0)

#walls must be constructed after tesselation wrapper
walls = utils.aabbWalls([(0,0,0),(l,d,h)], thickness = 3)
O.bodies.append(walls)
for wall in walls:
	wall.material = O.materials[wall_mat]

O.bodies.erase(walls[5].id)
w_left = walls[0]
w_left.material = O.materials[w_left_mat]
    

def coloring():
	EF.aabbEnlargeFactor = 1
	DF.interactionDetectionFactor = 1
	for i in spheres:
		z = O.bodies[i].state.pos[2]

        
		if z <= 7.5:
			O.bodies[i].shape.color = (0.1, 0, 1)

		elif 7.5 < z <= 15:
			O.bodies[i].shape.color = (0.9, 1, 0)

		elif 15 < z <= 22.5:
			O.bodies[i].shape.color = (0.3, 1, 1)

		elif 22.5 < z <= 30:
			O.bodies[i].shape.color = (0.7, 0, 1)

		elif 30 < z <= 37.5:
			O.bodies[i].shape.color = (0.5, 1, 0)

		elif 37.5 < z:
			O.bodies[i].shape.color = (1, 1, 1)


	ctr.command = 'push()'

def push():
	global base
	w_pos = w_left.state.pos[0]
	base = 'T%.1f_C%.1f_BA%.1f_WA%.1f_ENLARGE%.2f_%.2f%%' % (TENSILESTRENGTH/1e6,COHESION/1e6,baseFrictAng,wallFrictAng,Enlarge,w_pos*100/l)
	snapShot.fileBase = vtkRecord.fileName = base
	O.engines = O.engines + [snapShot, vtkRecord]
	w_left.state.vel = (1, 0, 0)
	ctr.command = 'stop()'

def stop():
	global base
	w_pos = w_left.state.pos[0]
	base = 'T%.1f_C%.1f_BA%.1f_WA%.1f_ENLARGE%.2f_%.2f%%' % (TENSILESTRENGTH/1e6,COHESION/1e6,baseFrictAng,wallFrictAng,Enlarge,w_pos*100/l)
	snapShot.fileBase = vtkRecord.fileName = base
	if (O.iter - 2*pyRunnerPeriod)%savePeriod == 0:
		TW1.setState(1)
		TW1.defToVtk("cumulative"+base+".vtk")
		TW2.setState(1)
		TW2.defToVtk("periodical"+base+".vtk")
		TW2.setState(0)
		
		
	if w_pos > l*0.3:
		O.pause()
    
def crackRecorder():
	global base
	w_pos = w_left.state.pos[0]
	if O.iter < 2*pyRunnerPeriod:
		return
	if (O.iter - (2*pyRunnerPeriod - crackRecordPeriod) )%savePeriod == 0:
		OUT = 'T%.1f_C%.1f_BA%.1f_WA%.1f_ENLARGE%.2f_%.2f%%' % (TENSILESTRENGTH/1e6,COHESION/1e6,baseFrictAng,wallFrictAng,Enlarge,w_pos*100/l)
		interactionLaw.recordCracks = True
		interactionLaw.Key = vtkRecord.Key = OUT
	if (O.iter - 2*pyRunnerPeriod)%savePeriod == 0:
		interactionLaw.recordCracks = False