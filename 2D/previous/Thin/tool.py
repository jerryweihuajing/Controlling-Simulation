# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:17:56 2019

@author: whj
"""

import os
def GenerateFold(path):

    path=path.strip()
   
    path=path.rstrip("\\")

    Exist=os.path.exists(path)

    if not Exist:
        
        os.makedirs(path) 
