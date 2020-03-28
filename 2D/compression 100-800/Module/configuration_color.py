# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:09:18 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Color
"""

from configuration_spheres import n_layer

#yade rgb list
yade_rgb_list=[[0.50,0.50,0.50],
               [1.00,0.00,0.00],
               [0.00,1.00,0.00],
               [1.00,1.00,0.00],
               [0.85,0.85,0.85],
               [0.00,1.00,1.00],
               [1.00,0.00,1.00],
               [0.90,0.90,0.90],
               [0.15,0.15,0.15],
               [0.00,0.00,1.00]]

#grey: yade_rgb_list[4:5]
#black: yade_rgb_list[-2:-1]
#green: yade_rgb_list[2:3]
#yellow: yade_rgb_list[3:4]

base_rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[4:5]
lower_base_rgb_list=yade_rgb_list[-2:-1]+yade_rgb_list[5:6]
upper_base_rgb_list=yade_rgb_list[6:7]+yade_rgb_list[4:5]
deposit_rgb_list=yade_rgb_list[2:4]+yade_rgb_list[9:]+yade_rgb_list[0:1]+yade_rgb_list[5:7]

#proper number of layer
while len(base_rgb_list)<n_layer:

	base_rgb_list*=2
    
#proper number of layer
while len(upper_base_rgb_list)<n_layer:

	upper_base_rgb_list*=2

#proper number of layer
while len(lower_base_rgb_list)<n_layer:

	lower_base_rgb_list*=2
        
while len(deposit_rgb_list)<20:

	deposit_rgb_list*=2
    
rgb_uplift=yade_rgb_list[-1]
rgb_detachment=yade_rgb_list[1]
rgb_green=yade_rgb_list[2]
rgb_yellow=yade_rgb_list[3]