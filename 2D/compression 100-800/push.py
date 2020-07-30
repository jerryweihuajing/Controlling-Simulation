# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:42:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script-push
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'//Module')
sys.path=list(set(sys.path)) 

from operation_simulation import *

from configuration_material import *
from configuration_base import *
from configuration_salt import *
from configuration_fracture import *
from configuration_uplift import *
from configuration_motion import *
from configuration_model import *
from configuration_erosion import *
from configuration_deposit import *
from configuration_variable import *

O.run()

print('')
print('-- Simulation on')
print('-> case:',case_name)
print('')
