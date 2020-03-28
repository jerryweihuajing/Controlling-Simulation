# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:57:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Erosion
"""

def ErosionName(exp_name,case_name):
    
    exp_name+=' erosion'
    
    return exp_name,case_name

def Erosion(which_O,y_max):
    
    old_bodies=[1 for this_body in which_O.bodies if this_body!=None]
    
    spheres=[]  
    
    #create idx list for deleting
    idx_to_delete=[]
    
    for k in range(3,len(which_O.bodies)):

        if which_O.bodies[k]==None:
            
            continue
        
        if which_O.bodies[k].state.pos[1]>y_max:
        
            idx_to_delete.append(k)
            
        else:
            
            spheres.append(O.bodies[k])
            
    print ''
    print 'before delete'
    print 'amount of bodies:',len(old_bodies)   
    
    #delete from O.bodies
    for this_idx in idx_to_delete:
        
        which_O.bodies.erase(this_idx)
        
    new_bodies=[1 for this_body in which_O.bodies if this_body!=None]
    
    print ''
    print 'after delete'
    print 'amount of bodies:',len(new_bodies)
    print 'amount of spheres:',len(spheres)
    
    return spheres