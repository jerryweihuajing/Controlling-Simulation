# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:25:56 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Simulation
"""

from configuration_container import *            
from configuration_motion import *
from configuration_deposit import *
from configuration_erosion import *
from configuration_record import *

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
                                        deposit_width,\
                                        deposit_offset,\
                                        deposit_period)'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder] 

#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation(deposit,
                   erosion,
                   deposit_thickness,
                   deposit_width,
                   deposit_offset,
                   deposit_period):
    
    offset=box_length-(wall_right.state.pos[0]-wall_left.state.pos[0]) #wall ypos
    progress=(offset/box_length)*100

    print('iter',O.iter)
    print('the offset is %.2f' %offset)
    print('the progress is %.2f%%' %progress)
    print()

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
            
            print()
            print('-- Simulation off')
            
        #make deposition 
        if O.iter>savePeriod and deposit and (O.iter==deposit_period*savePeriod+3*checkPeriod): #front mountain
        
            #save the state every 10% of the progress
            x_max = max([this_sphere.state.pos[0] for this_sphere in spheres])
            y_max = max([this_sphere.state.pos[1] for this_sphere in spheres])
            x_min = min([this_sphere.state.pos[0] for this_sphere in spheres])
            y_min = min([this_sphere.state.pos[1] for this_sphere in spheres])
                    
            #adding deposit -----
            deposit_pack = pack.SpherePack()

            deposit_pack.makeCloud((x_max-deposit_offset-deposit_width, y_max, 0),
                                   (x_max-deposit_offset, y_max+2*deposit_thickness,0),
                                   rMean = 1, rRelFuzz = 0.2)
            
            deposit_pack.toSimulation(material = m_rock)
    
            print('amount of deposit',len(deposit_pack))
        
            spheres_deposit=[O.bodies[idx] for idx in range(len(O.bodies)-len(deposit_pack),len(O.bodies))]
                
            for this_sphere in spheres_deposit:
                
                this_sphere.shape.color=rgb_green