# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:25:56 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Simulation
"""

from operation_record import *

from configuration_container import *            
from configuration_motion import *
from configuration_deposit import *
from configuration_erosion import *
from configuration_variable import *

from minieigen import *

#------------------------------------------------------------------------------
"""
Function to start pushing

Args:
    None

Returns:
    None
"""
def StartPushing():
    
    print ''
    print '-- Start Pushing'
    
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
        
    controller.command = 'CheckPushing()'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder] 
    
#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation    
#------------------------------------------------------------------------------
"""
Function to stop pushing

Args:
    None

Returns:
    None
"""
def CheckPushing():
    
    print ''
    print '-- Check Pushing'
    
    offset=box_length-(wall_right.state.pos[0]-wall_left.state.pos[0]) #wall ypos
    progress=(offset/box_length)*100

    print ''
    print 'iter',O.iter
    print 'the offset is %.2f' %offset
    print 'the progress is %.2f%%' %progress
    print ''

    if O.iter%savePeriod==0:

        RecordData(open(folder_name+'/A_progress=%.2f%%' %progress+".txt",'w'))
        
    if O.iter%savePeriod==3*checkPeriod:

        #make erosion
        if O.iter>savePeriod and erosion and (O.iter==erosion_period*savePeriod+3*checkPeriod): 

            Erosion()
       
        RecordData(open(folder_name+'/B_progress=%.2f%%' %progress+".txt",'w'))
        
        #end the loop
        if O.iter==7*savePeriod+3*checkPeriod:

            O.pause()
            
            print ''
            print '-- Simulation off'
            
        #make deposition 
        if O.iter>savePeriod and deposit and (O.iter==deposit_period*savePeriod+3*checkPeriod): 
        
            Deposit()
            