# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:31:53 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Base
"""

base_thickness=2.4

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""  
def BaseName(exp_name,case_name):
    
    exp_name+=' base'
		
    case_name+=' bT='+str(base_thickness)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Base2Spheres():
    
    print ''
    print '-- Base to Spheres'
    
    from configuration_model import id_spheres
    from configuration_color import rgb_detachment
    from configuration_material import m_detachment
    from configuration_variable import uplift
    
    #with uplift
    if uplift:
        
        from configuration_uplift import map_height_uplift

        for i in id_spheres:
    
            this_x=O.bodies[i].state.pos[0]
            this_y=O.bodies[i].state.pos[1]
       
            if map_height_uplift[int(this_x)]<=this_y<=map_height_uplift[int(this_x)]+base_thickness:
                
                O.bodies[i].shape.color = rgb_detachment
                O.bodies[i].material = O.materials[m_detachment]  
                
    else:
        
        for i in id_spheres:
            
            if this_y<=O.bodies[i].state.pos[1]:
                
                O.bodies[i].shape.color = rgb_detachment
                O.bodies[i].material = O.materials[m_detachment]  