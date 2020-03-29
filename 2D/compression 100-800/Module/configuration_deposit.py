# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:54:49 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Deposit
"""

from yade import pack

deposit_thickness=10
deposit_offset=200
deposit_width=200
deposit_period=1

#------------------------------------------------------------------------------
"""
Expand case name from the factor

Args:
    exp_name: original exp name
    case_name: original case name

Returns:
    newly case and exp name
"""
def DepositName(exp_name,case_name):
    
    exp_name+=' deposit'
    
    case_name+=' dT='+str(deposit_thickness)
    case_name+=' dO='+str(deposit_offset)
    case_name+=' dW='+str(deposit_width)
    case_name+=' dP='+str(deposit_period)
    
    return exp_name,case_name

#------------------------------------------------------------------------------
"""
Deposit spheres

Args:
    spheres: sphere objects as base

Returns:
    newly case and exp name
"""
def Deposit():
    
    print ''
    print '-- Deposit'
    
    from configuration_color import rgb_green
    from configuration_material_compression import m_rock
    
    old_spheres=[O.bodies[k] for k in range(3,len(O.bodies)) if O.bodies[k]!=None]
    
    print ''
    print 'before adding'
    print 'amount of spheres:',len(old_spheres) 
    
    x_max = max([this_sphere.state.pos[0] for this_sphere in old_spheres])
    y_max = max([this_sphere.state.pos[1] for this_sphere in old_spheres])
    x_min = min([this_sphere.state.pos[0] for this_sphere in old_spheres])
    y_min = min([this_sphere.state.pos[1] for this_sphere in old_spheres])
            
    #adding deposit -----
    deposit_pack = pack.SpherePack()
    
    deposit_pack.makeCloud((x_max-deposit_offset-deposit_width, y_max, 0),
                           (x_max-deposit_offset, y_max+2*deposit_thickness,0),
                           rMean = 1, rRelFuzz = 0.2)
    
    deposit_pack.toSimulation(material = m_rock)
    
    print ''
    print 'amount of deposit',len(deposit_pack)
    
    spheres_deposit=[O.bodies[idx] for idx in range(len(O.bodies)-len(deposit_pack),len(O.bodies))]
        
    for this_sphere in spheres_deposit:
        
        this_sphere.shape.color=rgb_green
        
    new_spheres=[O.bodies[k] for k in range(3,len(O.bodies)) if O.bodies[k]!=None]
    
    print ''
    print 'after adding'
    print 'amount of spheres:',len(new_spheres)
    
#------------------------------------------------------------------------------
"""
Assign the parameter to spheres model

Args:
    None

Returns:
    None
"""
def Deposit2Spheres():
    
    print ''
    print '-- Deposit to Spheres'