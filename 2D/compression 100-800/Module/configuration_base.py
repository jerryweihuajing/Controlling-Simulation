# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:31:53 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Base
"""

base_thickness=10

def BaseName(exp_name,case_name):
    
    exp_name+=' base'
		
    case_name+=' bT='+str(base_thickness)
    
    return exp_name,case_name

def BaseSpheres():
    
    from configuration_uplift import map_height_uplift
    from configuration_sphere import id_spheres
    from configuration_color import rgb_detachment
    from configuration_matetrial import m_detachment
    
    for i in id_spheres:
    
        #O.bodies[i].state.blockedDOFs='XYz'
        
        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
        
        y_min=map_height_uplift[int(this_x)]
        y_max=map_height_uplift[int(this_x)]+base_thickness
        
        if y_min<=this_y<=y_max:
            
            O.bodies[i].shape.color = rgb_detachment
            O.bodies[i].material = O.materials[m_detachment]  