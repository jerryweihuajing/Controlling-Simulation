

#from yade import qt, pack, export
from yade import pack, export, plot
import math

#cai shen yang 2016
csyoung=1e10
cspoisson=0.3
csdensity=2500.0
csfric=0.6 #math.radians(18)
csnormalCohesion=5e7
csshearCohesion=5e7

#building walls -----
box_length = 15000.0
box_depth  = 10000.0
#adding deposit -----
sample_height = 8000.0 #not the final thickness 
box_height = 2.0*sample_height

################################################################################
MatWall   = O.materials.append(FrictMat(young=csyoung,
                                        poisson=cspoisson,
                                        frictionAngle=csfric,
                                        density=0,
                                        label='frictionWalls'))
MatWallFricless   = O.materials.append(FrictMat(young=csyoung,
                                        poisson=cspoisson,
                                        frictionAngle=0.0,
                                        density=0,
                                        label='frictionlessWalls'))
MatSphere = O.materials.append(CohFrictMat( young=csyoung,
                                            poisson=cspoisson,
                                            density=csdensity,
                                            frictionAngle=csfric,
                                            normalCohesion=csnormalCohesion,
                                            shearCohesion=csshearCohesion,
                                            label='spheres'))
struct_mat= O.materials.append(CohFrictMat( young=csyoung,
                                            poisson=cspoisson,
                                            density=csdensity,
                                            frictionAngle=0.0,
                                            normalCohesion=0.0,
                                            shearCohesion=0.0,
                                            label='struct'))
#gen ball
sample = pack.SpherePack()
sample.makeCloud((-box_depth/2, 0.0, 0.0), 
                 (box_depth/2, box_length , box_height),
                 rMean = 100.0, rRelFuzz = 1.0/4.0)#,num=10
rMean = 100.0
rRelFuzz = 1.0/4.0
#s60 = sample60.toSimulation(material = MatSphere)
#sample80 = pack.SpherePack()
#sample.makeCloud((0.0, 0.0, 0.0), 
#                 (0.0, box_length , box_height),
#                 rMean = 60, rRelFuzz = 0,porosity=0.6)#,num=10
s = sample.toSimulation(material = MatSphere)
#gen wall
sph_num=len(O.bodies)
wall_left  = wall(0.0,axis=1,sense=0,material=MatWall)
wall_right = wall(box_length,axis=1,sense=0,material=MatWall)
wall_bottom= wall(0.0,axis=2,sense=0,material=MatWallFricless)

wall_back  = wall(-box_depth/2,axis=0,sense=0,material=MatWallFricless)
wall_front = wall(box_depth/2,axis=0,sense=0,material=MatWallFricless)

O.bodies.append(wall_left)
O.bodies.append(wall_right)
O.bodies.append(wall_bottom)

O.bodies.append(wall_back)
O.bodies.append(wall_front)

#remember wall id

f1=facet([[box_depth/2,0,0],[box_depth/2,box_length/2.0,0],[-box_depth/2.0,0,0]],fixed=True,color=[1,0,0],material=MatSphere)
f2=facet([[-box_depth/2,0,0],[-box_depth/2,box_length/2.0,0],[box_depth/2.0,box_length/2.0,0]],fixed=True,color=[1,0,0],material=MatSphere)
f3=facet([[-box_depth/2.0,box_length/2.0,0],[-box_depth/2,box_length,0],[box_depth/2.0,box_length/2.0,0]],fixed=True,color=[1,0,0],material=MatSphere)
f4=facet([[box_depth/2,box_length/2.0,0],[-box_depth/2,box_length,0],[box_depth/2.0,box_length,0]],fixed=True,color=[1,0,0],material=MatSphere)
O.bodies.append([f1,f2,f3,f4])
wallsid=range(sph_num,len(O.bodies))

print 'bodies_num:',len(O.bodies)
#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  
#for i in s60:
    #a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
#    O.bodies[i].state.blockedDOFs='xYZ'
#for i in s:
#    O.bodies[i].state.blockedDOFs='xYZ'

#defining engines -----
thres = 40000
checkPeriod=1000
O.engines = [
    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Wall_Aabb()]),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom6D(), Ig2_Wall_Sphere_ScGeom()],
        [Ip2_FrictMat_FrictMat_FrictPhys(),Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(label="cohesiveIp")],
        [Law2_ScGeom_FrictPhys_CundallStrack(),Law2_ScGeom6D_CohFrictPhys_CohesionMoment(label='cohesiveLaw')]
    ),
    NewtonIntegrator(damping = 0.4, gravity = (0, 0, -9.81)),
    PyRunner(command = 'modifyLayer()', iterPeriod = 1000, label = 'controller'),
    ]

O.dt = utils.PWaveTimeStep()
#vtkRecorder = VTKRecorder(fileName='0.00%-',
#                          recorders=['spheres','colors','velocity',
#                                     'mass','stress','materialId','intr'],
#                          ascii=True,iterPeriod=10000)
                          
#O.engines = O.engines +[vtkRecorder]

TW1 = TesselationWrapper() #TW1 records cumulative strain data

TW2 = TesselationWrapper() #TW2 records periodical strain data







#display = qt.Renderer()
#display.intrPhys=True
#display.wire=True

#glv0=qt.View(); print 'Created view'
##glv0.grid=True,True,False; print 'grid x,y'
#glv0.axes=True; print 'axes shown'
#glv0.screenSize=800,800; print 'screen size set to 200x200'
#glv0.eyePosition=(box_length,box_length/2,0); 
#glv0.upVector=(0,0,1); 
#glv0.viewDir=(-1,0,0);
#glv0.center(True); print 'median center' # median center - will fallback since there are only 2



#pushing stage -----
v = 1.0

total_iter=int(box_length/(abs(v)*O.dt))
savePeriod=int((total_iter)/40)
savePeriod=int(savePeriod/checkPeriod)*checkPeriod
if savePeriod == 0:
    savePeriod =1000
print(savePeriod)
#snapshot = qt.SnapshotEngine(fileBase='-',iterPeriod=savePeriod)
#vtkRecorder = VTKRecorder(fileName='0.00%-',recorders=['all'],ascii=True,iterPeriod=savePeriod)
vtkRecorder = VTKRecorder(fileName='0.00%-',
                          recorders=['spheres','colors','velocity',
                                     'mass','stress','materialId','intr'],
                          ascii=True,iterPeriod=savePeriod)
#print savePeriod

def startPushing():
    

    #if O.iter < thres:
    #    return
    wall_right.state.vel = Vector3(0, v, 0)
    f3.state.vel = Vector3(0, v, 0)
    f4.state.vel = Vector3(0, v, 0)
    wall_left.state.vel = Vector3(0, -v, 0)
    f1.state.vel = Vector3(0, -v, 0)
    f2.state.vel = Vector3(0, -v, 0)
    controller.command = 'stopSimulation()'
    #O.engines = O.engines +[snapshot, vtkRecorder]
    O.engines = O.engines +[vtkRecorder]
  #  for i in s:
   #     if O.bodies[i].state.pos[2] < rMean*(1.1+rRelFuzz):
    #       # O.bodies[i].state.vel=(0,0,1000)
     #       if (0.5*box_length) < O.bodies[i].state.pos[1] :
              #  print("123")
      #          O.bodies[i].state.vel=(0,v,0)

#point in polygon
#yes return ture
#no  return false
def isInsidePolygon(pt, poly):
    c = False
    i = -1
    l = len(poly)
    j = l - 1
    while i < l-1:
        i += 1
        #print i,poly[i], j,poly[j]
        #print poly[0]
        if ((poly[i]["lat"] <= pt["lat"] and pt["lat"] < poly[j]["lat"]) or (poly[j]["lat"] <= pt["lat"] and pt["lat"] < poly[i]["lat"])):
            if (pt["lng"] < (poly[j]["lng"] - poly[i]["lng"]) * (pt["lat"] - poly[i]["lat"]) / (poly[j]["lat"] - poly[i]["lat"]) + poly[i]["lng"]):
                c = not c
        j = i
    return c

def coloring():
    cohesiveIp.setCohesionNow = True
    maxh = max([O.bodies[i].state.pos[2] for i in s])
    #coloring the sample -----
    for i in s:
        O.bodies[i].material = O.materials[MatSphere]
        O.bodies[i].shape.color = (1, 1, 1)
        if   sample_height*0/10 <= O.bodies[i].state.pos[2] < sample_height*1/10:
            O.bodies[i].shape.color = (1, 1, 1)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*1/10 <= O.bodies[i].state.pos[2]< sample_height*2/10:
            O.bodies[i].shape.color = (0.75, 1, 0)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*2/10 <= O.bodies[i].state.pos[2]< sample_height*3/10:
            O.bodies[i].shape.color = (0.5, 0, 1)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*3/10 <= O.bodies[i].state.pos[2]< sample_height*4/10:
            O.bodies[i].shape.color = (1, 1, 1)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*4/10 <= O.bodies[i].state.pos[2]< sample_height*5/10:
            O.bodies[i].shape.color = (0.75, 1, 0)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*5/10 <= O.bodies[i].state.pos[2]< sample_height*6/10:
            O.bodies[i].shape.color = (0.5, 0, 1)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*6/10 <= O.bodies[i].state.pos[2]< sample_height*7/10:
            O.bodies[i].shape.color = (1, 1, 1)
        elif sample_height*7/10 <= O.bodies[i].state.pos[2]< sample_height*8/10:
            O.bodies[i].shape.color = (0.75, 1, 0)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*8/10 <= O.bodies[i].state.pos[2]< sample_height*9/10:
            O.bodies[i].shape.color = (0.5, 0, 1)
            #O.bodies[i].material = O.materials[rock]
        elif sample_height*9/10 <= O.bodies[i].state.pos[2]< maxh:
            O.bodies[i].shape.color = (1, 1, 1)
            #O.bodies[i].material = O.materials[rock]
        
    #pre-existing structure
    pt={}
    for i in s:
        extend = 300.0
        if (-box_depth) < O.bodies[i].state.pos[0] < 0.0:
            pt['lat'] = O.bodies[i].state.pos[1]
            pt['lng'] = O.bodies[i].state.pos[2]
            poly = [{'lat':( box_length*10/20), 'lng':sample_height*2/10},
                    {'lat':( box_length*10/20+extend), 'lng':sample_height*2/10},
                    {'lat':( box_length*5/20+extend), 'lng':sample_height*8/10},
                    {'lat':( box_length*5/20), 'lng':sample_height*8/10}]
            if isInsidePolygon(pt, poly):
                O.bodies[i].material = O.materials[struct_mat]
                O.bodies[i].shape.color = (0.25, 0.2, 0.1)
        if 0.0 < O.bodies[i].state.pos[0] < box_depth:
            pt['lat'] = O.bodies[i].state.pos[1]
            pt['lng'] = O.bodies[i].state.pos[2]
            poly = [{'lat':(box_length*16/20), 'lng':sample_height*2/10},
                    {'lat':(box_length*16/20+extend), 'lng':sample_height*2/10},
                    {'lat':(box_length*11/20+extend), 'lng':sample_height*8/10},
                    {'lat':(box_length*11/20), 'lng':sample_height*8/10}]
            if isInsidePolygon(pt, poly):
                O.bodies[i].material = O.materials[struct_mat]
                O.bodies[i].shape.color = (0.25, 0.2, 0.1)
    #    if 0 <= O.bodies[i].state.pos[2] < 7.5:
    #        O.bodies[i].shape.color = (1, 1, 1)
    #        #O.bodies[i].material = O.materials[MatSphere]

    #    elif 7.5 <= O.bodies[i].state.pos[2]< 15:
    #        O.bodies[i].shape.color = (0.75, 1, 0)
    #        #O.bodies[i].material = O.materials[MatSphere]
    #            
    #    elif 15 <= O.bodies[i].state.pos[2]< 22.5:
    #        O.bodies[i].shape.color = (0.5, 0, 1)
    #        #O.bodies[i].material = O.materials[MatSphere]
    #            
    #    elif 22.5 <= O.bodies[i].state.pos[2]<= maxh:
    #        O.bodies[i].shape.color = (0.25, 1, 1)
    #        #O.bodies[i].material = O.materials[MatSphere]
                                    
    print "The max length is %.3f" % maxh

    controller.command = 'startPushing()'

def modifyLayer():

    plot.addData(
        unbalanced=utils.unbalancedForce(),
        i=O.iter,
    )

    if O.iter%1000 == 0:
        step = 'O.iter %d' % (O.iter)
        print step
        step = 'O.iter %d' % (O.iter)
        #vtkRecorder.fileName = step+'-' #record the current progress
        
    if O.iter < thres:
        return
    if O.iter > 60000:
        controller.command='coloring()'
        TW1.setState(0)
        TW1.setState(1)
        TW1.defToVtk("start.vtk")
        TW2.setState(0)
        #O.pause()
    for i in s:
        if O.bodies[i].state.pos[2] > sample_height:
            O.bodies.erase(i) #delete spheres that are above the target height
            s.remove(i) #also,delete the corresponding ids in the id list
    export.text('ini.txt')   
    #csExport('ini')
    
plot.plots={'i':('unbalanced',)}


    

#wallid=[0,1,2,3,4]

wallid=wallsid
def csExport(fileName):
    #fileName="%d" % (O.iter)
    global ids,wallsid
    ids =[]
    vtkExporter = export.VTKExporter('cs',startSnap=O.iter)
    #wall don't have radius
    #ids = [O.bodies[i].id for i in s]
    #vtkExporter.exportSpheres(what=[#('pos','b.state.pos'),
                                    #('radius','b.radius'),
                                    #
                                    #('mass','b.state.mass'),
                                    #('vel','b.state.vel'),
                                    #('angMom','b.state.angMom'),
                                    #('angVel','b.state.angVel'),
                                    #('dist','b.state.pos.norm()'),
                                    #('color','b.shape.color'),
                                    #])
#vtkExporter.exportFacets(what=[('pos','b.state.pos')])
    #if interaction num is 0 , this command will wrong!
    #vtkExporter.exportInteractions(what=[('kn','i.phys.kn')])
    #wall don't have cohesionBroken    
  #  ids = [(i.id1,i.id2) for i in O.interactions]
    #for i in O.interactions:
       # print(type(O.bodies[i.id1].material))
     #   if type(O.bodies[i.id1].material) == 'yade.wrapper.CohFrictMat'and type(O.bodies[i.id2].material) =='yade.wrapper.CohFrictMat':
      #      print ('asd')
       #     ids.append(i)
    print('wallsid',wallsid)
   # print('ids',ids)
   # ids=[]
   # for i in ids:
     #   print(i)
    #    if i[0] in wallsid or i[1] in wallsid:
          #  idsdel.append((i,j))
   #         print('asd')
        #    ids.remove(i)
    #print(idsdel)
  #  print('/n')

    ids = [(i.id1,i.id2) for i in O.interactions]
    idsdel=[]
    for i,j in ids:
        if i in wallsid or j in wallsid:
            idsdel.append((i,j))
    for i in idsdel:
        ids.remove(i)
    vtkExporter.exportInteractions(ids,what=[('kn','i.phys.kn'),('cohesionBroken','i.phys.cohesionBroken')])
    
#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation():
    #global flag
    #global count
   
    #save the state every 10% of the progress
    #if int(((l/box_length)*100)%10) == 0 and flag:
    #    name = "%d0%%.yade" % count
    #    count += 1
    #    O.save(name)
    #    flag = 0
    #if ((l/box_length)*100)%10 > 1:
    #    flag = 1
        
    #saving the strain data
    w_pos = wall_right.state.pos[1]
    w_pos1 = wall_left.state.pos[1]
    l = -w_pos1 + w_pos
    if (O.iter == 1 ):
        csExport('ini_iter_1')
    #print w_pos,(O.iter- thres),savePeriod,(O.iter- thres)%savePeriod
    if (O.iter- thres)%1000 == 0:
        step = 'O.iter %d' % (O.iter)
        print step
    if (O.iter- thres)%savePeriod == 0:
        #progress = "%.2f%%" % ((l/box_length)*100)
        progress = '%.2f%%' % (l*100/box_length)
        print progress
        #snapshot.fileBase = 
        vtkRecorder.fileName = 'doc-' #record the current progress
        csExport(progress)
        TW1.setState(1)
        TW1.defToVtk("cumulative%d"%O.iter+progress+".vtk")
        TW2.setState(1)
        TW2.defToVtk("periodical"+progress+".vtk")
        TW2.setState(0)
        
    
    if l > 1.5 * box_length:
        os.system("yade vtkProcessor.py")
        O.pause()
        

#plot.plot()
O.run(800000,True)

