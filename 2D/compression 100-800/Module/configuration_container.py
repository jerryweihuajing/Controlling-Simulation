# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:02:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Container
"""

from configuration_material import m_wall

#building boxes -----
box_length = 800.0
box_height = 100.0
box_depth  = 5

#wallMask
#determines which walls will be created, in the order
#-x(1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the
#default 63 means to create all walls
#parameter1:center
#parameter2:size
box = geom.facetBox(( box_length/2, box_height/2,0),
                    ( box_length/2, box_height/2,box_depth/2),
                    wallMask = 0,
                    material = m_wall)

#push plane
wall_right = utils.wall(box_length, axis = 0, material = m_wall)
wall_left = utils.wall(0, axis = 0, material = m_wall)
wall_bottom= utils.wall(0, axis = 1, material = m_wall)

O.bodies.append(wall_right)
O.bodies.append(wall_left)
O.bodies.append(wall_bottom)