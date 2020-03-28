# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:42:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Script-Initialization
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
sys.path=list(set(sys.path)) 

import operation_path as O_P

from configuration_material import *
from configuration_base import *
from configuration_salt import *
from configuration_fault import *
from configuration_uplift import *
from configuration_motion import *
from configuration_sphere import *
from configuration_erosion import *
from configuration_deposit import *
from configuration_simulation import *
from configuration_varaible import *