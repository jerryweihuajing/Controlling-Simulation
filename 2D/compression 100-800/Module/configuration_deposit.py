# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:54:49 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Deposit
"""

deposit_thickness=10
deposit_offset=200
deposit_width=200
deposit_period=1

def DepositName(exp_name,case_name):
    
    exp_name+=' deposit'
    
    case_name+=' dT='+str(deposit_thickness)
    case_name+=' dO='+str(deposit_offset)
    case_name+=' dW='+str(deposit_width)
    case_name+=' dP='+str(deposit_period)
    
    return exp_name,case_name