# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:07:10 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Motion
"""

from yade import utils
from yade.wrapper import *

v= 4 #default 0.4

#defining engines -----
savePeriod = int(8000*1.6/abs(v)) # save files for every iterPeriod steps
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
PyRunner(command = 'StartPushing()', iterPeriod = checkPeriod, label = 'controller'),
]

#snapshot = qt.SnapshotEngine(fileBase='-',iterPeriod=savePeriod)
#vtkRecorder = VTKRecorder(fileName='0.00%-',recorders=['all'],iterPeriod=savePeriod)

#O.dt =3* utils.PWaveTimeStep()
O.dt=0.0027

#TW1 = TesselationWrapper() #TW1 records cumulative strain data
#TW1.setState(0)
#TW1.setState(1)
#TW1.defToVtk("./cumulative strain/start.vtk")

#TW2 = TesselationWrapper() #TW2 records periodical strain data
#TW2.setState(0)