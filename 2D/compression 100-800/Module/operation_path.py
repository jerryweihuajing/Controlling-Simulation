# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:37:08 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Path Operation
"""

import os

#------------------------------------------------------------------------------
"""
Generate folder based on the given path

Args:
    path: path to generate folder

Returns:
    None
"""
def GenerateFold(path):

    print ''
    print '-- Generate Fold'
    
    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path)