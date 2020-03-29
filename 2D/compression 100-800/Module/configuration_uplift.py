# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:02:32 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Uplift
"""

from configuration_model import maxl

uplift_height=20
uplift_width=100
uplift_offset=100

#define uplift
k_uplift=uplift_height/uplift_width

#map between x and y
map_height_uplift={}

for k in range(int(maxl)):
    
    if k<uplift_width:
        
        map_height_uplift[k]=uplift_height-k_uplift*k
    
    else:
        
        map_height_uplift[k]=0

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""
def UpliftName(exp_name,case_name):
    
    exp_name+=' uplift'
    
    case_name+=' uH='+str(uplift_height)
    case_name+=' uW='+str(uplift_width)
    case_name+=' uO='+str(uplift_offset)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Uplift2Spheres():
    
    print ''
    print '-- Uplift to Spheres'
    
    from configuration_model import id_spheres
    from configuration_color import rgb_uplift
    from configuration_uplift import map_height_uplift
    from configuration_compression_matetrial import m_uplift
      
    for i in id_spheres:
    
        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
        
        y_min=0
        y_max=map_height_uplift[int(this_x)]
 
        if y_min<=this_y<=y_max:
            
            O.bodies[i].shape.color = rgb_uplift
            O.bodies[i].material = O.materials[m_uplift]

            O.bodies[i].state.blockedDOFs='xyz'