# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:44:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Fault
"""

import numpy as np

from configuration_sphere import maxl

fault_start_depth=50
fault_end_depth=0
fault_offset=200
fault_inclination=30

#map between y and x tuple
map_fault_y_x={}

k=np.tan(fault_inclination*np.pi/180)

if k>0:
    
    b=fault_start_depth-k*(maxl-fault_offset)
    
if k<0:
    
    b=fault_end_depth-k*(maxl-fault_offset)
    
fault_width=np.abs(3/np.sin(fault_inclination*np.pi/180))

for this_y in range(fault_end_depth,fault_start_depth):
    
    this_x=(this_y-b)/k
    
    map_fault_y_x[int(this_y)]=(this_x-fault_width/2,this_x+fault_width/2)
    
def FaultName(exp_name,case_name):
    
    exp_name+=' fault'
	
    case_name+=' fI='+str(fault_inclination)
    case_name+=' fO='+str(fault_offset)
    case_name+=' fD='+str(fault_end_depth)+'-'+str(fault_start_depth)
    
    return exp_name,case_name
    
def FaultSpheres():
    
    from configuration_model import id_spheres
    from configuration_color import rgb_detachment
    from configuration_matetrial import m_detachment
    
    for i in id_spheres:

        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]

        if int(this_y) in list(map_fault_y_x.keys()):
            
            x_min=map_fault_y_x[int(this_y)][0]
            x_max=map_fault_y_x[int(this_y)][1]
                
            if x_min<=this_x<=x_max:
  
                O.bodies[i].shape.color = rgb_detachment
                O.bodies[i].material = O.materials[m_detachment] 