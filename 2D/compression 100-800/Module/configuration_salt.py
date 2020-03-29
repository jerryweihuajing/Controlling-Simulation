# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:25:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Salt
"""

salt_thickness=10
salt_depth=25
salt_offset=0
salt_width=800

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""
def SaltName(exp_name,case_name):
    
    exp_name+=' salt'
    		
    case_name+=' sT='+str(salt_thickness)
    case_name+=' sD='+str(salt_depth)
    case_name+=' sO='+str(salt_offset)
    case_name+=' sW='+str(salt_width)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Salt2Spheres():
    
    from configuration_model import id_spheres,maxl
    from configuration_color import rgb_detachment
    from configuration_matetrial import m_detachment
    
    y_min=salt_depth
    y_max=salt_depth+salt_thickness
    x_min=maxl-salt_offset-salt_width
    x_max=maxl-salt_offset
    
    for i in id_spheres:

        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
    
        if y_min<=this_y<=y_max and x_min<=this_x<=x_max:
    		
            O.bodies[i].shape.color = rgb_detachment
            O.bodies[i].material = O.materials[m_detachment]
