# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:31:53 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Base
"""

base_thickness=2.4

def BaseName(exp_name,case_name):
    
    exp_name+=' base'
		
    case_name+=' bT='+str(base_thickness)
    
    return exp_name,case_name

def Base2Spheres():
    
    from configuration_model import id_spheres
    from configuration_color import rgb_detachment
    from configuration_material import m_detachment
    
    for i in id_spheres:

        this_y=O.bodies[i].state.pos[1]
 
        if this_y<=base_thickness:
            
            O.bodies[i].shape.color = rgb_detachment
            O.bodies[i].material = O.materials[m_detachment]  