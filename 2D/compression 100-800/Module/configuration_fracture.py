# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:44:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Fracture
"""

import numpy as np

from configuration_model import maxl

fracture_start_depth=50
fracture_end_depth=0
fracture_offset=200
fracture_inclination=30

#map between y and x tuple
map_fracture_y_x={}

k=np.tan(fracture_inclination*np.pi/180)

if k>0:
    
    b=fracture_start_depth-k*(maxl-fracture_offset)
    
if k<0:
    
    b=fracture_end_depth-k*(maxl-fracture_offset)
    
fracture_width=np.abs(3/np.sin(fracture_inclination*np.pi/180))

for this_y in range(fracture_end_depth,fracture_start_depth):
    
    this_x=(this_y-b)/k
    
    map_fracture_y_x[int(this_y)]=(this_x-fracture_width/2,this_x+fracture_width/2)

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""   
def FractureName(exp_name,case_name):
    
    exp_name+=' fracture'
	
    case_name+=' fI='+str(fracture_inclination)
    case_name+=' fO='+str(fracture_offset)
    case_name+=' fD='+str(fracture_end_depth)+'-'+str(fracture_start_depth)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""    
def Fracture2Spheres():
    
    print ''
    print '-- fracture to Spheres'
    
    from configuration_model import id_spheres
    from configuration_color import rgb_detachment
    from configuration_material import m_detachment
    
    for i in id_spheres:

        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]

        if int(this_y) in list(map_fracture_y_x.keys()):
            
            x_min=map_fracture_y_x[int(this_y)][0]
            x_max=map_fracture_y_x[int(this_y)][1]
                
            if x_min<=this_x<=x_max:
  
                O.bodies[i].shape.color = rgb_detachment
                O.bodies[i].material = O.materials[m_detachment] 