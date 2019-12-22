from yade import pack, qt, export
import math,sys

#geometric parameters-----
l = 600 #box length
d = 4 #box depth
h = 200 #box height
sample_h = 45 # samle height
young = 5e9
O.materials.append(JCFpmMat(
    type = 0,
    young = 50e12,
    poisson = 1,
    frictionAngle = math.atan(18),
    label = 'wall'
    ))

walls = utils.aabbWalls([(0,0,0),(l,d,h)],thickness = 10,material = 'wall')
O.bodies.append(walls)

O.bodies.erase(walls[5].id)


#particle parameters -----
    
O.materials.append(JCFpmMat(
    type = 0,
    young = young,
    poisson = 1.0/3,
    frictionAngle = 0,
    density = 4800,
    label = 'spheres'))
    
sp = pack.SpherePack()
sp.makeCloud((0,0,0), (l,d,200), rMean = 0.75, rRelFuzz=1.0/3)
spheres = sp.toSimulation(material = 'spheres')


#engines -----
O.engines = [
    ForceResetter(),
    InsertionSortCollider([Bo1_Box_Aabb(),Bo1_Facet_Aabb(),Bo1_Sphere_Aabb(aabbEnlargeFactor=1,label='EF')]),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=1,label='DF'),Ig2_Box_Sphere_ScGeom(), Ig2_Facet_Sphere_ScGeom()],
        [Ip2_JCFpmMat_JCFpmMat_JCFpmPhys()],
        [Law2_ScGeom_JCFpmPhys_JointedCohesiveFrictionalPM()]
    ),
    GlobalStiffnessTimeStepper(active=1, timeStepUpdateInterval=100, timestepSafetyCoefficient=0.5),
    NewtonIntegrator(damping = 0.4, gravity = (0,0,-9.81)),
    PyRunner(command = 'deposition()', iterPeriod = 300, label = 'ctr')
    ]
    

def deposition():
    if O.iter < 40000 or utils.unbalancedForce() > 0.3:
		sys.stdout.write('\rUnbalanced Force: %.4f             ' % utils.unbalancedForce())
		sys.stdout.flush()
		return
    ctr.command = 'checkHeight()'

lastDens = 0        
def checkHeight():
    global lastDens
    M = 0
    for i in spheres:
        if O.bodies[i].state.pos[2] > sample_h:
            O.bodies.erase(i)
            spheres.remove(i)
        else:
        	M += O.bodies[i].state.mass
    dens = M/(l*d*sample_h)
    print "Density: %.3f" % dens
    print "Sample Height: %.3f" % max([O.bodies[i].state.pos[2] for i in spheres])

    if dens == lastDens: 	#if the density doesn't change anymore, export the file
        export.text('dens%dYoung%.1fGPaL%dH%d.txt' % (dens,young/1e9,l,sample_h))
    else:
        lastDens = dens
