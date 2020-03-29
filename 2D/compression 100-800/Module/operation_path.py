# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:37:08 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Path Operation
"""

import os

def GenerateFold(path):

    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path)