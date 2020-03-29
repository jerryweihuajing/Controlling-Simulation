# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:23:27 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Operation-Record
"""

import math

from yade._utils import *
from yade.wrapper import *

#------------------------------------------------------------------------------
"""
Record all data via txt

Args:
    out_file: output file
    
Returns:
    None
"""
def RecordData(out_file):
    
    which_spheres=[O.bodies[k] for k in range(3,len(O.bodies)) if O.bodies[k]!=None]
    
    print ''
    print 'Record Data'
    print 'amount of spheres:',len(which_spheres)
    
    #TW records stress data
    TW=TesselationWrapper()
    TW.computeVolumes()
    stress=bodyStressTensors()

    for this_sphere in which_spheres:

        this_stress=stress[this_sphere.id]*4.*math.pi/3.*this_sphere.shape.radius**3/TW.volume(this_sphere.id)

	    #print(this_stress)
	    
	    #id
        out_file.write(str(this_sphere.id))  
        out_file.write(',')

	    #radius
        out_file.write(str(this_sphere.shape.radius))

	    #color
        for this_color in this_sphere.shape.color:

            out_file.write(',')
            out_file.write(str(this_color))
	    
	    #position
        for this_pos in this_sphere.state.pos:

            out_file.write(',')
            out_file.write(str(this_pos))

        #velocity
        for this_vel in this_sphere.state.vel:

            out_file.write(',')
            out_file.write(str(this_vel))
        
        #stress
        for this_line in this_stress:
            
            for this_str in this_line:
                
                out_file.write(',')
                out_file.write(str(this_str))

        out_file.write('\n')