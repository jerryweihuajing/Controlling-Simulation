# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:22:33 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Model
"""

from yade import ymport

#num of layer
n_layer=10

#adding deposit -----
spheres = ymport.text('./sample.txt')
id_spheres = O.bodies.append(spheres)

#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  
for i in id_spheres:
    
	#a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
	O.bodies[i].state.blockedDOFs='XYz'

maxl = max([O.bodies[i].state.pos[0] for i in id_spheres])
maxh = max([O.bodies[i].state.pos[1] for i in id_spheres])

#coloring the sample -----
height_step=maxh/(n_layer)

print("The max height is %.3f" % maxh)
print("The max length is %.3f" % maxl)

#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Model2Spheres():
    
    print ''
    print 'Model to Spheres'
    
    from configuration_color import base_rgb_list
    from configuration_uplift import map_height_uplift
    from configuration_material_compression import m_rock
    
    #so many conditions
    for i in id_spheres:

        this_x=O.bodies[i].state.pos[0]
        this_y=O.bodies[i].state.pos[1]
        
        O.bodies[i].state.blockedDOFs='XYz'
    
        for k in range(n_layer):
    
            this_x=O.bodies[i].state.pos[0]
            this_y=O.bodies[i].state.pos[1]
            
            if k*height_step<=this_y<=(k+1)*height_step:
                
                O.bodies[i].shape.color = base_rgb_list[k]
                O.bodies[i].material = O.materials[m_rock]