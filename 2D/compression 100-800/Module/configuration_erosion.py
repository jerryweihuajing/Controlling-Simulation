# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:57:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Erosion
"""

erosion_period=1

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""
def ErosionName(exp_name,case_name):
    
    exp_name+=' erosion'
    
    case_name+=' eP='+str(erosion_period)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Erode spheres who are higher than y_max

Args:
    None
    
Returns:
    None
"""
def Erosion():
    
    print ''
    print '-- Erosion'
    
    old_spheres=[O.bodies[k].state.pos[1] for k in range(3,len(O.bodies)) if O.bodies[k]!=None]
    
    y_max=0.8*max(old_spheres)
    
    new_spheres=[]  
    
    #create idx list for deleting
    idx_to_delete=[]
    
    for k in range(3,len(O.bodies)):

        if O.bodies[k]==None:
            
            continue
        
        if O.bodies[k].state.pos[1]>y_max:
        
            idx_to_delete.append(k)
            
        else:
            
            new_spheres.append(O.bodies[k])
            
    print ''
    print '-> before delete'
    print '-> amount of spheres:',len(old_spheres)   
    
    #delete from O.bodies
    for this_idx in idx_to_delete:
        
        O.bodies.erase(this_idx)
          
    print ''
    print '-> after delete'
    print '-> amount of spheres:',len(new_spheres)
    
#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Erosion2Spheres():
    
    print ''
    print '-- Erosion to Spheres'