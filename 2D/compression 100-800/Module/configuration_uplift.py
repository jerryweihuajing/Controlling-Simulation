# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:02:32 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Uplift
"""

import numpy as np

from configuration_container import box_length

uplift_height=20
uplift_width=100
uplift_offset=500

'''up lift-shape of semi-sphere'''
#curvate radius
radius=(uplift_height**2+0.25*uplift_width**2)/(2*uplift_height)

#center of sphere
x_center=box_length-uplift_offset-0.5*uplift_width
y_center=(uplift_height**2-0.25*uplift_width**2)/(2*uplift_height)

#corner point of trapzoid
x_right=box_length-uplift_offset
x_left=box_length-uplift_offset-uplift_width

#map between x and y
map_height_uplift={}

for k in range(int(box_length)):
    
    map_height_uplift[k]=0
    
    if x_left<=k<=x_right:

        map_height_uplift[k]=y_center+np.sqrt(radius**2-(k-x_center)**2)
        
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
    from configuration_material import m_uplift
      
    for i in id_spheres:
    
        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
        
        y_min=0
        y_max=map_height_uplift[int(this_x)]
 
        if y_min<=this_y<=y_max:
            
            O.bodies[i].shape.color = rgb_uplift
            O.bodies[i].material = O.materials[m_uplift]

            #these spheres remain still
            O.bodies[i].state.blockedDOFs='xyz'